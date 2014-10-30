from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


README = read('README.rst')
CHANGES = read('CHANGES.rst')


setup(
    name="django-js-utils",
    packages=find_packages(),
    version="0.1",
    url="https://github.com/ISKME/django-js-utils",
    description="django_js_utils is a small utility library that aims to "
                "provide JavaScript/Django developers with a few utilities "
                "that will help the development of RIA on top of a Django "
                "Backend.",
    long_description="\n\n".join([README, CHANGES]),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords=["javascript"],
    include_package_date=True
)
