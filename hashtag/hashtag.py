"""The hashtag module

Two types of hashtags: static and ad-hoc
Static hashtags are

The hashtag system consists of groups of hashtags

Each group contains:
- The group name
- Group type:
    - either static or dynamic
        (this decides which users can edit the group)
- A set of hashtags

Example System:
    Group 1:
        - Group name: "Resource type"
        - Group type: static
        - hashtags: "video", "pdf", etc.
    Group 2:
        - Group name: "Concepts"
        - Group type: dynamic
        - hashtags: "NLP", "language model", etc.
"""
import re

import editdistance

THRESHOLD = 0.3


def _clean(s):
    """preprocess surface of hashtag for editdistance metric"""
    s = re.sub(r'\W+', '', s)
    return s.lower()


def _recommend_with_single_hashtag(query, pool, processed_pool_surface, k=1):
    query = _clean(query)
    dist = [editdistance.eval(query, tag) for tag in processed_pool_surface]
    res = sorted(range(len(dist)), key=lambda i: dist[i])[:k]
    return [pool[i] for i in res if dist[i] / len(query) < THRESHOLD]


def recommend_hashtag(queries, hashtag_pool):
    pool = hashtag_pool
    # pool = database.retrieve_concepts()
    processed_pool_surface = [_clean(surface) for _, surface in pool]
    recommended = []
    for query in queries:
        recommended.extend(_recommend_with_single_hashtag(
            query, pool, processed_pool_surface))
    return recommended
