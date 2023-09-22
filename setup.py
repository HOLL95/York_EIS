from setuptools import setup, find_packages
setup(
    # Module name (lowercase)
    name='YorkEIS',

    # List of dependencies
    install_requires=[
        'numpy>=1.8',
        'pints>=0.5.0',
        'matplotlib>=1.5',
        "pandas"
    ],
    python_requires='>=3.7',
)
