from setuptools import setup, find_packages

setup(
    name='HorseRace',
    version='1.0.0',
    description='A horse race terminal toy screen saver thing',
    author='Nixietab',
    url='https://github.com/nixietab/horserace',
    packages=find_packages(),
    py_modules=['horserace'],
    entry_points={
        'console_scripts': [
            'horserace = horserace:main',
        ],
    },
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
