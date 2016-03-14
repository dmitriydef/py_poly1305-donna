import sys
import os
from setuptools import (
    setup,
    find_packages, Extension,
)


os.chdir(os.path.dirname(sys.argv[0]) or ".")

'''
==============================================================================
PACKAGE DATA
==============================================================================
'''
module_name = 'poly1305_donna'
long_description = open('README.rst').read()
author = 'Sundar Nagarajan'
author_email = 'sun.nagarajan@gmail.com'
url = 'https://github.com/sundarnagarajan/py_poly1305-donna'
version = '0.1'
install_requires = [
    'cffi>=1.0.0',
    'six>=1.9.0'
],

'''
==============================================================================
SOURCE LOCATIONS
==============================================================================
'''
c_dir = 'floodberry.poly1305_donna'
libname = 'libpoly1305donna'
c_src_files = [
    'poly1305-donna.c',
]
libpath = os.path.join(module_name, libname)
c_src_list = [os.path.join(c_dir, x) for x in c_src_files]


setup(
    name=module_name,
    version=version,
    description=module_name,
    long_description=long_description,
    url=url,
    author=author,
    author_email=author_email,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=install_requires,
    packages=find_packages(),
    zip_safe=False,
    ext_modules=[
        Extension(
            libpath,
            c_src_list,
            include_dirs=[c_dir],
        )],
)
