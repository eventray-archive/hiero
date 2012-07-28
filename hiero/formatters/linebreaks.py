class LinebreaksFormatter(object):
    def __init__(self, text):
        self.text = text

    def get_html(self):
        """
        This parses out new lines and replaces them with html breaks
        """
        return self.text.replace('\n', '<br />')
