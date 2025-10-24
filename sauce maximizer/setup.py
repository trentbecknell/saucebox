from setuptools import setup, find_packages

setup(
    name="saucemax",
    version="0.1.0",
    author="SauceMax Team",
    description="Simple audio analysis tool for mix enhancement",
    url="https://github.com/trentbecknell/saucemax",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
    ],
    entry_points={
        "console_scripts": [
            "saucemax=cli:main",
        ],
    },
)