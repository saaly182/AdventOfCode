#!/usr/bin/python3
"""
Libary to process input as blank-line-separated multiline records.
"""


def multiline_file(filename):
    """
    Generator of multiline records that use blank lines as the
    record separator. Return each record as a string with newlines
    intact, and treat all blank lines as non-records.
    """
    with open(filename, 'r') as f:
        # r is the multiline record
        r = ''
        for line in f:
            if line == '\n':
                if r:
                    yield r
                    r = ''
            else:
                r += line
        if r:
            yield r


def multiline_data(iterable):
    """
    Generator of multiline records that use blank elements as the
    record separator. Return each record as a tuple of strings,
    and treat all blank lines as non-records.
    """
    r = []
    for x in iterable:
        if x.strip() == '':
            if r:
                yield tuple(r)
                r = []
        else:
            r.append(x)
    if r:
        yield tuple(r)
