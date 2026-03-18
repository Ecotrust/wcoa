import os
from setuptools import find_packages, setup

base_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(base_dir, 'README.md')) as readme:
    README = readme.read()


def read_requirements(path):
    requirements = []
    with open(path) as requirements_file:
        for raw_line in requirements_file:
            line = raw_line.strip()
            if not line or line.startswith('#') or line.startswith('-e '):
                continue
            requirements.append(line)
    return requirements

install_requires = read_requirements(os.path.join(base_dir, 'wcoa', 'requirements.txt'))

setup(
    name='wcoa',
    version='0.1',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app for wcoa.',
    long_description=README,
    url='https://www.wcoa.com/',
    author='Your Name',
    author_email='yourname@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: X.Y',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
