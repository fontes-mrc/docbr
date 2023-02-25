import setuptools

with open("README.md", "r", encoding="utf-8") as r:
    long_description = r.read()

setuptools.setup(
    name="docbr",
    version="0.1.3",
    license="MIT License",
    author="Maurício Adriano Fontes",
    author_email="suporte@mfontes.dev",
    description="Validate Brazilian documents at scale.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fontes-mrc/docbr",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy>=1.22.2'],
    python_requires='>=3.8'
)