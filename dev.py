import json

from submission import DevSubmission

IS_DEV = True

DIR_DEV_DAT = 'dat/consented_submissions.json'


def load_dev_dat():
    raw_dat = json.load(open(DIR_DEV_DAT, 'r'))
    return [DevSubmission(dat) for dat in raw_dat]


def load_cs410_concepts():
    """Return list of CS410 concepts (the list is not clean)"""
    with open('dat/cs410_concept.txt') as f:
        ret = [line.strip() for line in f.readlines()]
    return ret


def pseudo_on_resource_added(dat):
    """Returns a fake document ID"""
    import time
    return str(time.time())