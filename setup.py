from setuptools import setup, find_packages

setup(
    name='friday_night',
    description='Track watched and want-to-watch media.',
    version='0.0.1',
    author='Landon West',
    author_email='landonewest@gmail.com',
    url='https://github.com/landonwest/friday-night',
    packages=find_packages(exclude=['tests']),
    test_suite='test',
)
