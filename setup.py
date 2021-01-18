from setuptools import setup

def readme():
    with open("README.md", "r") as f:
        return f.read().encode("utf-8")

setup(name="occasionally",
        version="v0.0.1",
        # description="A task scheduling system implemented using only stdlib.",
        long_description=readme(),
        long_description_content_type="text/markdown",
        classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers'
        ],
        url="https://github.com/dleonard203/occasionally",
        author="Dave Leonard",
        keywords="task scheduler",
        license="MIT",
        packages=["occasionally"],
        zip_safe=True
)