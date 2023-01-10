"""
Unittest module to test Hooks.

Requires the unittest, pytest, and requests-mock Python libraries.

Run test:

    python3 -m unittest tests.hooks.test_sample_hook.TestSampleHook

"""

import logging
import unittest
from unittest import mock

# Import Hook
from airflow_provider_pulumi.hooks.automation import PulumiAutoHook

log = logging.getLogger(__name__)


# Mock the `conn_sample` Airflow connection
@mock.patch.dict(
    "os.environ",
    AIRFLOW_CONN_PULUMI_DEFAULT="pulumi://:pul-token@/?extra__pulumi__project_name=my-project&extra__pulumi__stack_name=dev&extra__pulumi__config_passphrase=pass",
)
@mock.patch.dict(
    "os.environ",
    AIRFLOW_CONN_PULUMI_S3="pulumi://s3%3A%2F%2Fpulumi-bucket%2F%3Fregion%3Dus-west-2/?extra__pulumi__project_name=my-project&extra__pulumi__stack_name=dev",
)
@mock.patch.dict("os.environ", PULUMI__PULUMI_CONFIG_PASSPHRASE="env-pass")
class TestPulumiAutoHook(unittest.TestCase):
    """
    Test Pulumi Auto Hook.
    """

    def test_pulumi_service_backend(self):
        # Instantiate hook
        hook = PulumiAutoHook(
            pulumi_program=lambda x: None, pulumi_conn_id="pulumi_default"
        )

        # Pulumi Hook's get_conn method returns a Stack
        stack = hook.get_conn()

        # Assert the stack name is set
        assert stack.name == "dev"

        # Assert the project is set
        assert hook.project_name == "my-project"

        # Assert env vars are set
        assert hook.env_vars["PULUMI_ACCESS_TOKEN"] == "pul-token"
        assert hook.env_vars["PULUMI_CONFIG_PASSPHRASE"] == "pass"

    @mock.patch("pulumi.automation.create_or_select_stack")
    def test_pulumi_cloud_backend(self, mock_create_stack):
        # Instantiate hook
        hook = PulumiAutoHook(pulumi_program=lambda x: None, pulumi_conn_id="pulumi_s3")

        # Pulumi Hook's get_conn method returns a Stack
        stack = hook.get_conn()

        # Assert the stack name is set
        assert hook.stack_name == "dev"

        # Assert the project is set
        assert hook.project_name == "my-project"

        # Assert env vars are set
        assert hook.env_vars["PULUMI_CONFIG_PASSPHRASE"] == "env-pass"

        # Assert backend url
        assert hook.backend_url == "s3://pulumi-bucket/?region=us-west-2"


if __name__ == "__main__":
    unittest.main()
