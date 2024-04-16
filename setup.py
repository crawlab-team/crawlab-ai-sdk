from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    install_requires = f.read().split('\n')

setup(
    name="crawlab-ai",
    version="0.0.9",
    packages=find_packages(),
    url="https://github.com/crawlab-team/crawlab-ai-sdk",
    license="MIT",
    author="Marvin Zhang",
    author_email="tikazyq@163.com",
    description="SDK for Crawlab AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"crawlab_ai": "crawlab_ai"},
    keywords=["crawlab", "ai"],
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "crawlab-ai=crawlab_ai.cli:main",
        ]
    },
)
