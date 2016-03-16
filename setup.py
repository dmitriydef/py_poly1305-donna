import sys
import os
from setuptools import setup, find_packages, Extension
import setupext


os.chdir(os.path.dirname(sys.argv[0]) or ".")

# See help.txt for detailed help on different sections
'''
==============================================================================
PACKAGE DATA
==============================================================================
'''
# You _SHOULD_ set these
toplevel = 'poly1305_donna'
version = '0.1'
description = toplevel
install_requires = [
    'cffi>=1.0.0',
    'six>=1.9.0',
]
packages = find_packages()
license = 'License :: OSI Approved :: MIT License'

# The following are optional
long_description = open('README.rst').read()
url = 'https://github.com/sundarnagarajan/py_poly1305-donna'
download_url = 'https://github.com/sundarnagarajan/py_poly1305-donna.git'
author = 'Sundar Nagarajan'
# author_email = ''
maintainer = author
# maintainer_email = author_email
classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: PyPy',
    'License :: OSI Approved :: MIT License',
]
zip_safe = True


'''
==============================================================================
C EXTENSION DETAILS

Put the C files in a dir under toplevel so that the C files can also be
installed using data_dirs (see ADDITIONAL DATA FILES)
==============================================================================
'''
c_dir = 'floodberry.poly1305_donna'
libname = 'libpoly1305donna'
c_src_files = [
    'poly1305-donna.c',
]
libpath = os.path.join(toplevel, libname)
c_src_list = [os.path.join(toplevel, c_dir, x) for x in c_src_files]
ext_modules = [
    Extension(
        name=libpath,
        sources=c_src_list,
        include_dirs=[c_dir],
    )
]


'''
==============================================================================
ADDITIONAL DATA FILES
---------------------

- set data_dirs to LIST of directories under toplevel that
    you want to include

see help.txt for more details
==============================================================================
'''

data_dirs = [
    'doc',
    'floodberry.poly1305_donna',
]


'''
==============================================================================
CUSTOM STEPS

see help.txt for more details
==============================================================================
'''


'''
==============================================================================
ADDITIONAL keyword args to setup()
==============================================================================
'''
ADDL_KWARGS = dict(
    py_modules=[setupext,],
)


'''
==============================================================================
           DO NOT CHANGE ANYTHING BELOW THIS
==============================================================================
'''

# Required keywords
kwdict = dict(
    name=toplevel,
    version=version,
    install_requires=install_requires,
    packages=packages,
    description=description,
    license=license,
)

# Optional keywords
kwdict.update(dict(
    long_description=globals().get('long_description', ''),
    url=globals().get('url', ''),
    download_url=globals().get('download_url', ''),
    author=globals().get('author', ''),
    author_email=globals().get('author_email', ''),
    maintainer=globals().get('maintainer', ''),
    maintainer_email=globals().get('maintainer_email', ''),
    classifiers=globals().get('classifiers', []),
    keywords=globals().get('keywords', []),
    zip_safe=globals().get('zip_safe', False),
))
kwdict.update(ADDL_KWARGS)

# To support custom step triggers
kwdict['cmdclass'] = setupext.get_cmdclass()

# More optional keywords, but which are added conditionally
ext_modules = globals().get('ext_modules', [])
if ext_modules:
    kwdict['ext_modules'] = ext_modules

dirlist = globals().get('data_dirs', None)
if isinstance(dirlist, list):
    kwdict['package_dir'] = {toplevel: toplevel}
    kwdict['package_data'] = {toplevel:
                              setupext.get_dirtree(toplevel, dirlist)}


setup(**kwdict)
