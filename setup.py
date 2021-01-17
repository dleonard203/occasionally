from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(name="occasionally",
        version="0.0.0",
        description="A task scheduling system implemented using only stdlib",
        long_description=readme(),
        long_description_content_type="text/markdown",
        # todo add classifiers
        classifiers=[],
        url="https://github.com/dleonard203/occasionally",
        author="Dave Leonard",
        keywords="task scheduler",
        license="MIT",
        packages=["occasionally"],
        zip_safe=True
)