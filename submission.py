class Submission:
    pass


class DevSubmission(Submission):
    def __init__(self, dat):
        self.url = dat['source_url']
        self.highlight = dat['highlighted_text']

