import os
import sys
from btfly import (
    __author__,
    __author_email__,
    __status__,
    __version__
)

def get_long_description():
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README')
    long_description = ''
    try:
        f = open(file)
        long_description = ''.join(f.readlines())
        f.close()
    except IOError:
        print 'Failed to open file "%s".' % (file)
        f.close()
    return long_description

try:
    from setuptools import setup
    setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

install_requires = [
    'PyYAML',
]

if sys.version_info < (2, 7):
    install_requires.append('argparse')

setup(
    name = 'btfly',
    version = __version__,
    url = 'http://github.com/oinume/btfly/',
    license = 'LGPL',
    author = __author__,
    author_email = __author_email__,
    description = "Manage your servers in YAML or JSON.",
    long_description = get_long_description(),
    packages = [ 'btfly' ],
    scripts = [ os.path.join('bin', p) for p in [ 'btfly' ] ],
    zip_safe = False,
    platforms = 'unix',
    install_requires = install_requires,
    tests_require = [
        'mock',
        'pytest',
    ],
#    test_suite = 'nose.collector',
# TODO: data_files
    data_files = [
        ( 'etc', [ 'conf/*.*' ] ),
        ( 'plugins', [ 'plugins/*.py' ] ),
    ],
    classifiers = [
        'Development Status :: 4 - ' + __status__,
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
    ],
)
