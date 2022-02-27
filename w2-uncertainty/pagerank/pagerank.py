import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def get_distinct_keys(dict):
    return set(key for key in dict.keys())


def round_dict_precision_4(dict):
  return {key:float(f'{dict[key]:.4f}') for key in dict}


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    tm = dict() # transition model (tm) initiation

    page_links = corpus[page] # used also further below if page has links
    page_links_count = len(page_links) # used also fruther below if page has links

    # if page has no links, return tm with equal probability for each page
    if page_links_count == 0:
        damping_factor = 0

    # likelihood for random pick of any link that isn't the current page
    all_links = get_distinct_keys(corpus) # all distinct links in the corpus
    all_links_count = len(all_links)
    for link in all_links:
        tm[link] = (1 / all_links_count * (1 - damping_factor))

    # add likelihood for pick of links on current page, if any
    if damping_factor != 0:
        for link in page_links:
            tm[link] += (1 / page_links_count * damping_factor)

    return tm


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # prepage a list of all pages in the corpus and get a random first current page
    all_pages = list(get_distinct_keys(corpus)) # all distinct pages in the corpus
    current_page = all_pages[random.randrange(0, len(all_pages))]

    # populate sample dict
    p_ranks = dict()
    for _ in range(n):
        try:
            p_ranks[current_page] += 1 / n
        except KeyError:
            p_ranks[current_page] = 1 / n
        
        # assign new current page based on transition model probabilities
        tm = transition_model(corpus, current_page, damping_factor)
        weights = tuple(tm[p] for p in all_pages)
        current_page = random.choices(all_pages, weights=weights, k=1)[0]
        
    return round_dict_precision_4(p_ranks)


def have_pageranks_changed_significantly(old_pr, new_pr, significance = 0.001):
    any_value_changed_significantly = False
    for (k_old, v_old) in old_pr.items():
        if abs(v_old - new_pr[k_old]) > significance:
            any_value_changed_significantly = True
    return any_value_changed_significantly


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # prepage a set of all pages in the corpus, get the length
    all_pages = get_distinct_keys(corpus) # all distinct pages in the corpus
    all_pages_count = len(all_pages)

    # prepate iterative dict and assign each page (1/total pages) probability to start with
    p_ranks = dict()
    for page in all_pages:
        p_ranks[page] = 1 / all_pages_count

    # iteratively calculate a page’s PageRank based on the PageRanks of all pages that link to it
    iter = True # will be set to false once changes aren't significant anymore
    while iter:
        # make a copy of the current page probabilities (because of mutation)
        old_p_rank = copy.deepcopy(p_ranks)

        # go through each page in the ranking
        for page in old_p_rank:
            # sum up probabilities of pages linking to the page
            new_prob_sum = 0
            for p, links in corpus.items():
                # if a page has no links, assume it has links to each page
                if len(links) == 0:
                    new_prob_sum += old_p_rank[p] / all_pages_count
                # if a page has links to this page, add it's probability of lining to this page
                elif page in links:
                    new_prob_sum += old_p_rank[p] / len(links)

            # calculate new ranking based on base probability (1-damping_factor) and probability sum
            new_rank = ((1 - damping_factor) / all_pages_count) + damping_factor * new_prob_sum

            # assign new ranking for each page
            p_ranks[page] = new_rank

        # keep looping if page ranks still changed significantly (default: 0.001+ for any page rank)
        iter = have_pageranks_changed_significantly(old_p_rank, p_ranks)

    return round_dict_precision_4(p_ranks)


if __name__ == "__main__":
    main()
