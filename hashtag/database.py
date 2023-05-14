"""Databases

Hashtag database:
- table of static hashtags: <HashtagID, Hashtag, GroupName>
- table of concept hashtags: <HashtagID, Hashtag>
- table of hashtag submission tuples <SubmissionID, HashtagID, IsConcept>
"""
import os
import sqlite3

import dev

_DIR = 'hashtag.db'

_TABLE_STATIC = 'StaticHashtags'
_TABLE_CONCEPT = 'ConceptHashtags'
_TABLE_SUBMISSION = 'HashtagSubmissionRelations'


def _connect():
    return sqlite3.connect(_DIR)


def _initialize_tables():
    connection = _connect()
    try:
        cursor = connection.cursor()
        cmd = 'CREATE TABLE IF NOT EXISTS '
        cmd += _TABLE_STATIC
        cmd += '(HashtagID INTEGER PRIMARY KEY, Hashtag TEXT, GroupName TEXT)'
        cursor.execute(cmd)
        cmd = 'CREATE TABLE IF NOT EXISTS '
        cmd += _TABLE_CONCEPT
        cmd += '(HashtagID INTEGER PRIMARY KEY, Hashtag TEXT)'
        cursor.execute(cmd)
        cmd = 'CREATE TABLE IF NOT EXISTS '
        cmd += _TABLE_SUBMISSION
        cmd += '(SubmissionID TEXT, HashtagID INTEGER, IsConcept INTEGER)'
        cursor.execute(cmd)
        connection.commit()
    finally:
        connection.close()


def _create_dummy_data():
    connection = _connect()
    try:
        cursor = connection.cursor()
        cmd = 'INSERT INTO ' + _TABLE_STATIC
        cmd += '(Hashtag, GroupName) VALUES (?, ?)'
        cursor.execute(cmd, ('html', 'Resource Type'))
        cursor.execute(cmd, ('pdf', 'Resource Type'))
        cursor.execute(cmd, ('video', 'Resource Type'))
        for i in range(1, 11):
            cursor.execute(cmd, (str(i), 'Lecture'))
        # load 410 concepts and write to db
        hashtags = dev.load_cs410_concepts()
        cmd = 'INSERT INTO ' + _TABLE_CONCEPT
        cmd += '(Hashtag) VALUES (?)'
        for hashtag in hashtags:
            cursor.execute(cmd, (hashtag,))
        connection.commit()
    finally:
        connection.close()


if not os.path.isfile(_DIR):
    conn = _connect()
    _initialize_tables()
    if dev.IS_DEV:
        _create_dummy_data()

_grouped_static_hashtags = None  # {'GroupName':[(id, hashtag),...]}
_static_hashtags = None  # {hashtagID: (group name, hashtag)}


def get_static_hashtags():
    global _grouped_static_hashtags
    global _static_hashtags
    if _grouped_static_hashtags is None:
        connection = _connect()
        try:
            cursor = connection.cursor()
            cmd = 'SELECT * FROM ' + _TABLE_STATIC
            cursor.execute(cmd)
            results = cursor.fetchall()
        finally:
            connection.close()
        _grouped_static_hashtags = {}
        _static_hashtags = {}
        for hashtag_id, hashtag, group_name in results:
            if group_name not in _grouped_static_hashtags:
                _grouped_static_hashtags[group_name] = []
            _grouped_static_hashtags[group_name].append((hashtag_id, hashtag))
            _static_hashtags[hashtag_id] = (group_name, hashtag)
    return _grouped_static_hashtags, _static_hashtags


def get_concepts():
    connection = _connect()
    try:
        cursor = connection.cursor()
        cmd = 'SELECT * FROM ' + _TABLE_CONCEPT
        cursor.execute(cmd)
        results = cursor.fetchall()  # hashtag id, hashtag
    finally:
        connection.close()
    return results


def _link_hashtags_to_submission(
        submission_id, hashtag_ids, is_concept):
    is_concept = 1 if is_concept else 0
    connection = _connect()
    try:
        cursor = connection.cursor()
        cmd = 'INSERT INTO ' + _TABLE_SUBMISSION
        cmd += '(SubmissionID, HashtagID, IsConcept) VALUES (?, ?, ?)'
        for hashtag_id in hashtag_ids:
            cursor.execute(cmd, (submission_id, hashtag_id, is_concept))
        connection.commit()
    finally:
        connection.close()


def link_static_hashtags_to_submission(submission_id, hashtag_ids):
    _link_hashtags_to_submission(submission_id, hashtag_ids, False)


def _link_concepts_to_submission(submission_id, hashtag_ids):
    _link_hashtags_to_submission(submission_id, hashtag_ids, True)


def add_concepts_to_submission(submission_id, hashtags):
    """
    :param submission_id:
    :param hashtags: List of concept surfaces (Hashtag column)
    """
    hashtags = list(set(hashtags))  # avoid duplication
    hashtag_ids = []
    connection = _connect()
    try:
        cursor = connection.cursor()
        # query if hashhag exists
        cmd_query = 'SELECT * FROM '+ _TABLE_CONCEPT + ' WHERE (Hashtag=?)'
        cmd_add = 'INSERT INTO ' + _TABLE_CONCEPT + ' (Hashtag) VALUES (?)'
        for hashtag in hashtags:
            cursor.execute(cmd_query, (hashtag, ))
            result = cursor.fetchone()
            if result is not None:
                hashtag_ids.append(result[0])
            else:
                cursor.execute(cmd_add, (hashtag,))
                hashtag_ids.append(cursor.lastrowid)
        connection.commit()
    finally:
        connection.close()
    _link_concepts_to_submission(submission_id, hashtag_ids)


def get_submission_hashtags(submission_id):
    """Returns the hashtags labeled to the queried submission
    TODO: update the contents
    """
    connection = _connect()
    try:
        cursor = connection.cursor()
        cmd = 'SELECT (HashtagID, IsConcept) ' \
              'FROM ' + _TABLE_SUBMISSION + ' WHERE SubmissionID=?'
        cursor.execute(cmd, submission_id)
        results = cursor.fetchall()
        static_ids = []
        concept_ids = []
        _, static_hashtags = get_static_hashtags()

    finally:
        connection.close()
    return results


if __name__ == '__main__':
    print(get_static_hashtags())
