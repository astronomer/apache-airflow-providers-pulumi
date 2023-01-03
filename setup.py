"""Setup.py for the Astronomer sample Airflow provider package. Built from datadog provider package for now."""

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

"""Perform the package airflow-provider-sample setup."""
setup(
    name="airflow-provider-pulumi",
    version="0.0.2",
    description="A Pulumi provider package built by Astronomer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "airflow_provider_pulumi": [
            "provider_info=airflow_provider_pulumi.__init__:get_provider_info"
        ]
    },
    license="Apache License 2.0",
    packages=[
        "airflow_provider_pulumi",
        "airflow_provider_pulumi.hooks",
        # "airflow_provider_pulumi.sensors",
        "airflow_provider_pulumi.operators",
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
