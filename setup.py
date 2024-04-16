from setuptools import setup, find_packages

setup(
    name="crawlab-ai",
    version="0.0.6",
    packages=find_packages(),
    url="https://github.com/crawlab-team/crawlab-ai-sdk",
    license="MIT",
    author="Marvin Zhang",
    author_email="tikazyq@163.com",
    description="SDK for Crawlab AI",
    package_dir={"crawlab_ai": "crawlab_ai"},
    keywords=["crawlab", "ai"],
    entry_points={
        "console_scripts": [
            "crawlab-ai=crawlab_ai.cli:main",
        ]
    },
)
