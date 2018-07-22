from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    
    return list(set(a.split('\n')).intersection(b.split('\n')))
    
def sentences(a, b):
    """Return sentences in both a and b"""
    
    return list(set(sent_tokenize(a)).intersection(sent_tokenize(b)))


def substring_tokenize(str, n):
    substrings = []

    for i in range(len(str) - n + 1):
        substrings.append(str[i:i + n])

    return substrings


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    a_substrings = set(substring_tokenize(a, n))
    b_substrings = set(substring_tokenize(b, n))

    return a_substrings & b_substrings
