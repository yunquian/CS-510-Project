import sys

from flask import Flask
from flask import request, jsonify
from werkzeug.exceptions import BadRequest

import dev
import hashtag.database as database
import hashtag.hashtag as hashtag
import hashtag.keyword_extraction as keyword_extraction

app = Flask(__name__)


def _get_json(object_type):
    try:
        # flask raises BadRequest if parse fails
        data = request.get_json()
        if not isinstance(data, object_type):
            raise BadRequest("Must be " + str(object_type))
        return data
    except BadRequest:
        return None


# @app.route('/api/hashtags', methods=['GET'])
# def get_static_hashtag_groups():
#     grouped_static_hashtags, _ = database.get_static_hashtags()


@app.route('/api/hashtags', methods=['GET', 'POST'])
def suggest_hashtags():
    print('On request received', flush=True)
    grouped_static_hashtags, _ = database.get_static_hashtags()
    concepts = database.get_concepts()

    dat = request.get_json()
    content = dat['content']
    highlight = dat['highlight']
    hashtag_pool = []
    if highlight != '':
        hashtag_pool.extend(
            keyword_extraction.extract_nouns_from_short_text(highlight))
    if content != '':
        hashtag_pool.extend(
            keyword_extraction.extract_concepts_from_document(content)
        )
    recommended_hashtags = hashtag.recommend_hashtag(hashtag_pool, concepts)
    extracted_hashtags = [(-1, item) for item in hashtag_pool]
    ret = {'static': grouped_static_hashtags, 'concepts': concepts,
           'recommend': recommended_hashtags + extracted_hashtags}
    print(recommended_hashtags + hashtag_pool, flush=True)
    return jsonify(ret), 200


@app.route('/api/submit', methods=['POST'])
def submit():
    if request.mimetype == 'application/json':
        submitted_dat = request.get_json()
        submission_id = dev.pseudo_on_resource_added(submitted_dat)  # TODO
        dat = submitted_dat['hashtag']
        static_hashtag_selected_states = dat['static_hashtag_selected_states']
        static_hashtag_ids = [
            int(k) for k, v in static_hashtag_selected_states.items() if v]
        concepts = dat['concepts']
        print(dat, flush=True)
        database.link_static_hashtags_to_submission(
            submission_id, static_hashtag_ids)
        database.add_concepts_to_submission(submission_id, concepts)
        # TODO: work with Kevin Ros to finalize the submission process
    return 'Success', 200

