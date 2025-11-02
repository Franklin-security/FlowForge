"""
Setup script for the application.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="flowforge",
    version="1.0.0",
    author="DevOps Team",
    description="FlowForge - Modern CI/CD Pipeline Orchestration Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Franklin-security/FlowForge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "flask>=3.0.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "pyyaml>=6.0.1",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "flowforge=src.main:main",
        ],
    },
)

