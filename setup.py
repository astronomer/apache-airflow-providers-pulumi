"""Setup.py for the Astronomer sample Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-sample setup."""
setup(
    name="airflow-providers-pulumi",
    version="0.0.1",
    description="A Pulumi provider package built by Astronomer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "airflow_provider": ["provider_info=pulumi_provider.__init__:get_provider_info"]
    },
    license="Apache License 2.0",
    packages=[
        "pulumi_provider",
        "pulumi_provider.hooks",
        # "pulumi_provider.sensors",
        "pulumi_provider.operators",
    ],
    install_requires=["apache-airflow>=2.0", "pulumi>=3.0.0,<4.0.0"],
    setup_requires=["setuptools", "wheel"],
    author="Dylan Intorf",
    author_email="dylan.intorf@astronomer.io",
    url="http://astronomer.io/",
    classifiers=[
        "Framework :: Apache Airflow",
        "Framework :: Apache Airflow :: Provider",
    ],
    python_requires="~=3.7",
)
