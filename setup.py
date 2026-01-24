"""
Setup configuration for Hobby Budget Tracker.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hobby-budget-tracker",
    version="0.1.0",
    author="HobbyBudgetTracker",
    description="A cross-platform application to track hobby budgets and activities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bohlke01/HobbyBudgetTracker",
    packages=find_packages(),
    package_data={
        "hobby_budget_tracker": ["templates/*", "static/*"],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "hobby-budget=hobby_budget_tracker.cli:main",
            "hobby-budget-web=hobby_budget_tracker.web:main",
        ],
    },
)
