import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from BeautifulSoup import BeautifulSoup

class HtmlCodeBlockFormatter(object):
    def __init__(self, text):
        self.text = text

    def pre_parse(self):
        """
        Parses out <code> blocks out of a block of text returns highlighted div
        list and a BeautifulSoup object for further parsing
        """
        index = 0
        last_index = 0
        escaped_blocks = []

        # Grab all code blocks, match <code> and <code class="foo">
        while index >= 0:
            index = self.text.find('<code', last_index)

            mid_index = self.text.find('>', index)
            last_index = self.text.find('</code>', mid_index)

            # Whats between <code> and </code>
            code_to_esc = self.text[mid_index + 1:last_index]

            lang = None

            lang_index = self.text[index:mid_index + 1].find('class=')

            if lang_index > 0:
                lang = self.text[index:mid_index + 1]
                lang = lang[lang_index + len('class="'):-2]

            if lang:
                try:
                    lexer = get_lexer_by_name(lang, stripnl=True,
                            encoding='UTF-8')
                except ValueError:
                    # We eat this exception because handling if a language
                    # wasn't found is the same as if this failed.
                    pass
            else:
                lexer = None

            if not lexer:
                lexer = get_lexer_by_name('text', stripnl=True,
                        encoding='UTF-8')

            formatter = HtmlFormatter(linenos=True,
                cssclass='source'
            )

            # Format the code as HTML and syntax highlight it
            escaped_code = highlight(code_to_esc, lexer, formatter)
            escaped_blocks.append(escaped_code)

            # re-check index< see if we have anymore
            index = self.text.find('<code', last_index)

        soup = BeautifulSoup(self.text)
        code_blocks = soup.findAll(u'code')

        # We have already formatted the code, don't allow the markup language
        # to do it a second time.
        for block in code_blocks:
            block.replaceWith(u'<code class="removed"></code>')

        # Pass it back though beautiful soup after replacing html nodes
        self.soup = BeautifulSoup(str(soup))
        self.escaped_blocks = escaped_blocks

    def post_parse(self):
        # Replace all the empty code blocks with the syntax highlighted html
        empty_code_blocks = self.soup.findAll('code', 'removed')
        for index, escaped_block in enumerate(self.escaped_blocks):
            empty_code_blocks[index].replaceWith(escaped_block)

    def get_html(self):
        self.pre_parse()
        self.post_parse()

        return str(self.soup)
