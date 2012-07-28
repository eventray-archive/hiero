import markdown


class MarkdownFormatter(object):
    def __init__(self, text):
        self.text = text

    def get_html(self):
        return markdown.markdown(self.text, ['codehilite'])
