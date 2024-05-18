from setuptools import setup, find_packages

setup(
    name="streamlit_voice",
    version="0.1.0",
    author="Jose Manuel Napoles",
    description="A Streamlit component for animated Avatars",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
