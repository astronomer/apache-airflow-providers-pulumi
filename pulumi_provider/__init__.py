## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "airflow-providers-pulumi",  # Required
        "name": "Pulumi Airflow Provider",  # Required
        "description": "A pulumi provider for airflow.",  # Required
        "connection-types": [
            {
                "hook-class-name": "pulumi_provider.hooks.pulumi_auto.PulumiHook",
                "connection-type": "pulumi",
            }
        ],
        "extra-links": [],
        "versions": ["0.0.1"],  # Required
    }
