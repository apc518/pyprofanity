from setuptools import setup

setup(
    name='profanity',
    version='0.1.0',
    description='A profanity detector Python package',
    url='https://github.com/apc518/pyprofanity',
    author='Andy Chamberlain',
    author_email='andychamberlainmusic@gmail.com',
    license='MIT',
    packages=['profanity'],
    install_requires=[],
    classifiers=[
        'License :: MIT',
        'Programming Language :: Python 3'
    ],
    include_package_data=True,
    package_data={ 'profanity': ['data/*.txt', 'data/*.json'] }
)