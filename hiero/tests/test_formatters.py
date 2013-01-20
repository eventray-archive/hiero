from unittest import TestCase
from mock import Mock
from hiero.formatters import get_formatter
from hiero.formatters.htmlblock_formatter import HtmlCodeBlockFormatter
from hiero.formatters.markdown_formatter import MarkdownFormatter
import re


class FormattersTests(TestCase):
    """
    Tests the basic functionality of our formatters
    """
    def setUp(self):
        pass

    def test_get_formatter(self):
        """
        Tests that the proper formatter is returned
        """
        formatters = ['MarkdownFormatter', 'LinebreaksFormatter',
                'HtmlCodeBlockFormatter']

        for formatter in formatters:
            obj = get_formatter(formatter)
            assert formatter != None
            self.assertEquals(formatter, obj.__name__)


class MarkdownTests(TestCase):
    def setUp(self):
        self.content = """Hello,

    #!python
        def foo(self):
            return 'bar'

foo bar baz

    :::python
        def foo(self):
            return 'bar'
        """
        self.formatter = MarkdownFormatter(self.content)

    def test_parses_code_blocks_properly(self):
        html = self.formatter.get_html()
        self.assertTrue(html.find('python') < 0)


class HtmlCodeBlockTests(TestCase):
    def setUp(self):
        self.content = """Hello, World.
        <code class="python">
            def foo(request):
                bar = 'baz'
                wibble = 0
                return bar
        </code>

        Does this work?

        <code>
            $ ls -a
            $ rm -rf
        </code>

        <code class="randomnamewontreturnlexer">
            // should figure out code type
            public static void Page_Load(object ender, EventArgs args) {
                return "HI";
            }
        </code>

        <code class="randomnamewontreturnlexer">
            !~ this isn't code ~!
        </code>
        """
        self.formatter = HtmlCodeBlockFormatter(self.content)

    def test_pre_parses_code_blocks(self):
        self.formatter.pre_parse()
        rb = '<code class="removed"></code>'
        removed_blocks = re.compile(rb).findall(str(self.formatter.soup))

        # Removed the code blocks and stored them already highlighted
        self.assertEqual(len(removed_blocks), 4)
        self.assertEqual(len(self.formatter.escaped_blocks), 4)

    def test_post_parse_adds_blocks_back(self):
        self.formatter.pre_parse()
        self.formatter.post_parse()

        rb = '<code class="removed"></code>'
        removed_blocks = re.compile(rb).findall(str(self.formatter.soup))

        # At this point we should've added the highlighted blocks back in
        self.assertEqual(len(removed_blocks), 0)

    def test_get_html_calls_all_parse_methods(self):
        self.formatter.soup = Mock()
        self.formatter.pre_parse = Mock()
        self.formatter.post_parse = Mock()
        self.formatter.get_html()

        self.formatter.pre_parse.assert_called_once_with()
        self.formatter.post_parse.assert_called_once_with()
