import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        result = pytest.main(self.test_args)
        sys.exit(result)

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid'
    , 'pyramid_debugtoolbar'
    , 'pyramid_tm'
    , 'waitress'
    , 'horus'
    , 'celementtree'
    , 'sqlalchemy'
    , 'psycopg2'
    , 'BeautifulSoup'
    , 'markdown'
    , 'docutils'
    , 'hem'
    , 'horus'
]

setup(
    name='hiero'
    , version='0.3.3'
    , description='hiero'
    , long_description=README + '\n\n' +  CHANGES
    , classifiers=[
        "Programming Language :: Python"
        , "Framework :: Pylons"
        , "Topic :: Internet :: WWW/HTTP"
        , "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ]
    , author='John Anderson'
    , author_email='sontek@gmail.com'
    , url=''
    , keywords='web pyramid pylons'
    , packages=find_packages()
    , include_package_data=True
    , zip_safe=False
    , install_requires=requires
    , cmdclass = {'test': PyTest}
    , tests_require=requires + ['pytest', 'mock', 'webtest']
    , test_suite="hiero"
    , dependency_links = [
        'https://github.com/eventray/hem/tarball/master#egg=hem-dev'
        , 'https://github.com/eventray/horus/tarball/master#egg=horus-dev'
    ]

    , entry_points = """\
    [paste.app_factory]
    main = hiero:main
    """
)

