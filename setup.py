from setuptools import setup, find_packages

with open('FinDataBroker/__about__.py') as file:
    about = {}
    exec(file.read(), about)

with open('README.md') as file:
    readme = file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    author=about['__author__'],
    license=about['__license__'],
    packages=find_packages(),
    install_requires=requirements,
    test_requires=['pytest'],
    python_requires='>=3.6',
    include_package_data=True,
    entry_points={'console_scripts': ["FinDataBroker = FinDataBroker.cli:main"]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business :: Financial',
        'Intended Audience :: Financial and Insurance Industry'
    ],
)
