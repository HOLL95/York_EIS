from setuptools import setup, find_packages
setup(
    # Module name (lowercase)
    name='YorkEIS',
    #packages=["eis_functions"],
    #py_modules=["EIS_class"],
    # List of dependencies
    install_requires=[
        'numpy>=1.8',
        'pints>=0.5.0',
        'matplotlib>=1.5',
        "pandas"
    ],
    python_requires='>=3.7',
)
def main():
    print("src")

if __name__ == '__main__':
    main()
