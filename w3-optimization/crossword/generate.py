from array import array
import sys
import random

from crossword import *

class CrosswordCreator():

    log_all = False

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        log = False

        # solve() logic
        self.enforce_node_consistency()

        # order_domain_values() and select_unassigned_variable() method dev test
        self.my_print(log, f"self.order_domain_values(): {self.order_domain_values(list(self.domains.keys())[random.randint(3,len(self.domains) - 1)], dict((k, v) for k, v in list(self.domains.items())[0:3]))}")
        self.my_print(log, f"self.select_unassigned_variable(): {self.select_unassigned_variable(dict((k, v) for k, v in list(self.domains.items())[0:3]))}")

        # solve() logic
        self.my_print(log, f"ac3(): domains BEFORE:', {self.domains}")
        is_problem_solvable = self.ac3()
        self.my_print(log, f"ac3(): domains AFTER:', {self.domains}is_problem_solvable: {is_problem_solvable}")
        if not is_problem_solvable:
            return None # don't try to backtrack if the problem is unsolvable

        # assignment_complete() and consistent() methods dev test
        self.my_print(log, f"self.assignment_complete(): {self.assignment_complete(self.domains)}")
        self.my_print(log, f"self.consistent(): {self.consistent(self.domains)}")

        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, words in self.domains.items():
            for word in words.copy():
                if len(word) is not variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        log = False
        self.my_print(log, f"-- revise() x: {x}, y: {y}")

        i, j = self.crossword.overlaps[x, y] # e.g. (0, 1)
        x_words = self.domains[x]
        y_words = self.domains[y]
        y_words_overlap_chars = set([y_word[j] for y_word in y_words])
        self.my_print(log, f"y_words_overlap_chars: {y_words_overlap_chars}")

        x_words_changed = False
        for x_word in x_words.copy():
            x_word_overlap_char = x_word[i]
            self.my_print(log, f"{x_word_overlap_char} in y_words_overlap_chars: {x_word_overlap_char in y_words_overlap_chars}")
            if x_word_overlap_char not in y_words_overlap_chars:
                self.domains[x].remove(x_word)
                x_words_changed = True

        self.my_print(log, f"-- x_words_changed: {x_words_changed}")
        return x_words_changed

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        log = False

        queue = arcs or self.domains.keys()
        self.my_print(log, f"ac3(): queue (arcs: {bool(arcs)}):", queue)

        for variable in queue:
            self.my_print(log, f"ac3(): variable:', {variable}")
            neighbors = self.crossword.neighbors(variable)
            self.my_print(log, f"ac3(): neighbors:', {neighbors}")

            variable_domain_words = self.domains.get(variable)
            for n in neighbors:
                x_words_changed = self.revise(variable, n)
                
                # if the variable has no words left in its domain, the problem is unsolvable
                variable_has_words_left = bool(variable_domain_words)
                if not variable_has_words_left:
                    return False

                # call this function again with all the changed variable's neighbors if the words of the variable's domain changed
                if x_words_changed: 
                    self.ac3(neighbors)
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # return all(len(words) == 1 for words in assignment.values()) # stricter check (each variable has exactly one word assigned to it)
        return all(bool(word_or_words) for word_or_words in assignment.values())

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        log = False

        assignment_vars = set()

        for var, word_or_words in assignment.items():
            self.my_print(log, f"var: {var}, word_or_words: {word_or_words}")

            self.my_print(log, f"len(word_or_words): {len(word_or_words)}, type(word_or_words): {type(word_or_words)}")
            # check if there is just one word assigned per variable
            if len(word_or_words) == 1:
                word = list(word_or_words)[0]
                self.my_print(log, f"word: {word}")
            else:
                return False

            # check if the word is unique (used just once in the assignment)
            if word in assignment_vars:
                return False
            else:
                assignment_vars.add(word)

            # ensure if the word has the correct length
            if len(word) is not var.length:
                return False
            
            # ensure there are no conflicts with neighboring variables
            for neighbor in self.crossword.neighbors(var):
                i, j = self.crossword.overlaps[var, neighbor] # e.g. (0, 1)
                self.my_print(log, f"neighbor: {neighbor}, i: {i}, j: {j}")
                neighbor_word = list(assignment[neighbor])[0]
                self.my_print(log, f"neighbor_word: {neighbor_word}, word[i]: {word[i]}, neighbor_word[j]: {neighbor_word[j]}")
                if word[i] is not neighbor_word[j]:
                    return False

        # otherwise, all checks have passed and the assignment is consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        log = False

        # get already assigned values in assignment
        # double list comprehension: [item for sublist in list for item in sublist]
        assignment_values = set(value for values in list(assignment.values()) for value in values)
        self.my_print(log, f"assignment_values: {assignment_values}")

        # get 
        self.my_print(log, f"var: {var}")
        var_values = self.domains[var] # words in that var's domain
        self.my_print(log, f"var_values: {var_values}")

        # var values - assignment values = possible values for var
        possible_values = var_values - assignment_values
        if len(possible_values) == 0:
            possible_values = var_values # this should probably not occur
        self.my_print(log, f"possible_values: {possible_values}")

        possible_values_rating = dict((value, 0) for value in possible_values)
        self.my_print(log, f"possible_values_rating: {possible_values_rating}")

        neighbor_vars = set(neighbor for neighbor in self.crossword.neighbors(var))
        self.my_print(log, f"neighbor_vars: {neighbor_vars}")
        assignment_vars = set(var for var in list(assignment.keys()))
        self.my_print(log, f"assignment_vars: {assignment_vars}")
        unassigned_neighbor_vars = neighbor_vars - assignment_vars
        if len(unassigned_neighbor_vars) == 0:
            unassigned_neighbor_vars = neighbor_vars # this should probably not occur
        self.my_print(log, f"unassigned_neighbor_vars: {unassigned_neighbor_vars}")

        for neighbor_var in unassigned_neighbor_vars:
            self.my_print(log, f"neighbor_var: {neighbor_var}")
            neighbor_values = self.domains[neighbor_var]
            self.my_print(log, f"neighbor_values: {neighbor_values}")

            i, j = self.crossword.overlaps[var, neighbor_var] # e.g. (0, 1)
            self.my_print(log, f"var inded i: {i}, neighbor var index j: {j}")

            for neighbor_value in neighbor_values:
                self.my_print(log, f"neighbor_value: {neighbor_value}")
                for possible_value in possible_values:
                    self.my_print(log, f"possible_value: {possible_value}")
                    if possible_value[i] is neighbor_value[j]:
                        possible_values_rating[possible_value] += 1

        self.my_print(log, f"possible_values_rating: {possible_values_rating}")
        return list(word[0] for word in sorted(possible_values_rating.items(), key=(lambda value: value[1]), reverse=True))


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        log = False

        assignment_vars = set(var for var in list(assignment.keys()))
        self.my_print(log, f"assignment_vars: {assignment_vars}")

        possible_vars = self.crossword.variables - assignment_vars
        self.my_print(log, f"possible_vars: {possible_vars}")

        var_dict = dict((var, {
            'values': self.domains.get(var),
            'value_count': len(self.domains.get(var)),
            'neighbor_count': len(self.crossword.neighbors(var))
        }) for var in possible_vars)
        self.my_print(log, f"var_dict: {var_dict}")

        return dict((var, data['values']) for var, data in sorted(var_dict.items(), key=(lambda item: (item[1]['value_count'], -item[1]['neighbor_count'])), reverse=False))


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        print('backtrack()')

    def my_print(self, log, *args):
        if self.log_all or log:
            [print(arg) for arg in args]
            print('')


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
