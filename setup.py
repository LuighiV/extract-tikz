import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="extracttikz",
    version="0.0.5",
    author="Luighi Viton-Zorrilla",
    author_email="luighiavz@gmail.com",
    description="Script to extract tikz from file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LuighiV/extract-tikz",
    project_urls={
        "Bug Tracker": "https://github.com/LuighiV/extract-tikz/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License ",
        "Operating System :: POSIX :: Linux ",
    ],
    packages=setuptools.find_packages(
        include=[
            'extracttikz',
            'extracttikz.*']),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        'colorlog',
        'python-dotenv'],
    entry_points={
        'console_scripts': [
            'extracttikz=extracttikz.cli:main',
        ],
    },
)
