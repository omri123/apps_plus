from setuptools import setup, find_packages

setup(
    name="apps_plus",
    version="0.1.0",
    description="A Python package for working with APPS+ data",
    author="Your Name",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        "apps_plus": ["../data/v1/data.json"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[],
    python_requires=">=3.7",
)
