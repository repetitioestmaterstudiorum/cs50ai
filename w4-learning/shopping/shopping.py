import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# testing some other classifiers (see train_model function)
# from sklearn.svm import SVC
# from sklearn.linear_model import Perceptron
# from sklearn.naive_bayes import GaussianNB

###
# Supervised learning exercise
###

TEST_SIZE = 0.4
K_NEAREST_NEIGHBORS = 1

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    evidence_train, evidence_test, label_train, label_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(evidence_train, label_train)
    predictions = model.predict(evidence_test)
    sensitivity, specificity = evaluate(label_test, predictions)

    # Print results
    print(f"Correct: {(label_test == predictions).sum()}")
    print(f"Incorrect: {(label_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")
    # print(f"Accuracy: {100 * (label_test == predictions).sum() / len(predictions):.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        labels = []
        for row in reader:
            evidence.append(get_evidence_values(row[:17]))
            labels.append(1 if row[17] == "TRUE" else 0)

        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=K_NEAREST_NEIGHBORS) # ~82% accuracy

    # testing some other classifiers (ensure imports are correct)
    # model = model = Perceptron() # ~88% accuracy
    # model = SVC() # ~84% accuracy
    # model = GaussianNB() # ~84% accuracy

    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    total_positive_labels = 0
    correct_positive_labels = 0
    total_negative_labels = 0
    correct_negative_labels = 0
    for l, p in zip(labels, predictions):
        if l == 1:
            total_positive_labels += 1
            if p == 1:
                correct_positive_labels += 1

        if l == 0:
            total_negative_labels += 1
            if p == 0:
                correct_negative_labels += 1

    # this could lead to division by 0 (totals could be 0 depending on data)
    true_positive_rate = 1 / total_positive_labels * correct_positive_labels
    true_negative_rate = 1 / total_negative_labels * correct_negative_labels

    return (true_positive_rate, true_negative_rate)


# helpers
def get_evidence_values(evidence):
    # print('--- evidence', evidence)
    i = 0
    evidence_values = []
    for cell in evidence:
        # string to int
        if i in [0, 2, 4, 11, 12, 13, 14]:
            evidence_values.append(int(cell))
        # string to float
        elif i in [1, 3, 5, 6, 7, 8, 9]:
            evidence_values.append(float(cell))
        # month to 0-11
        elif i == 10:
            evidence_values.append(get_month_as_number(cell))
        # visitor type to 1/0
        elif i == 15:
            evidence_values.append(1 if cell == 'Returning_Visitor' else 0)
        # weekend to 1/0
        elif i == 16:
            evidence_values.append(1 if cell == 'TRUE' else 0)
        else:
            IndexError(f"did not expect i of {i}")
        i += 1

    # print('evidence_values', evidence_values, '\n')
    return evidence_values


def get_month_as_number(month):
    month_to_number_dict = {
        'Jan': 0,
        'Feb': 1,
        'Mar': 2,
        'Apr': 3,
        'May': 4,
        'Jun': 5,
        'June': 5, # unclean data
        'Jul': 6,
        'Aug': 7,
        'Sep': 8,
        'Oct': 9,
        'Nov': 10,
        'Dec': 11,
    }
    return month_to_number_dict[month]


# not a helper :)
if __name__ == "__main__":
    main()
