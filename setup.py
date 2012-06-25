import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid'
    , 'pyramid_debugtoolbar'
    , 'waitress'
    , 'horus'
    ,'pyHAML'
    ,'pyramid_haml'
    ,'celementtree'
]

setup(
    name='hiero'
    , version='0.0'
    , description='hiero'
    , long_description=README + '\n\n' +  CHANGES
    , classifiers=[
        "Programming Language :: Python"
        "Framework :: Pylons"
        "Topic :: Internet :: WWW/HTTP"
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
    ]
    , author='John Anderson'
    , author_email='sontek@gmail.com'
    , url=''
    , keywords='web pyramid pylons'
    , packages=find_packages()
    , include_package_data=True
    , zip_safe=False
    , install_requires=requires
    , tests_require=requires
    , test_suite="hiero"
    , entry_points = """\
    [paste.app_factory]
    main = hiero:main
    [console_scripts]
    initdb = hiero.scripts.initdb:main
    """
)

