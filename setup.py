import os
from setuptools import setup, find_packages

def read_requirements(filename=None):
    if not filename:
        filename = "requirements.txt"

    requirements_file = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(requirements_file, "r") as rf:
            return [line.strip() for line in rf if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        raise RuntimeError("requirements.txt not found. Please ensure it exists.")

setup(
    name="cloudhive",
    version="0.0.1",
    author="Nitin Namdev",
    author_email="itsmyidbro@gmail.com",
    description="Some Useful Utils package",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/vortexdude/PyKit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
    install_requires=read_requirements(),  # Dynamically load dependencies from requirements.txt
    packages=find_packages(),  # Automatically discover all packages in the project
)
