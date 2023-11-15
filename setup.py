from setuptools import find_packages, setup

setup(
    name="Workulator",
    version="0.0.1",
    description="A workhour calculation tool",
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={"": [".gitignore"]},
    setup_requires=["setuptools-git"],
    install_requires=[
        "PyQt5",
        "setuptools",
        "appdirs",
        "pynput",
        "typing-extensions",
        "qtstylish>=0.1.2",
        "pywin32; platform_system=='Windows'",
        "black",
    ],
)
