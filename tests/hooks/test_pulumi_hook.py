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
from airflow_provider_pulumi.hooks.automation import PulumiHook

log = logging.getLogger(__name__)


# Mock the `conn_sample` Airflow connection
@mock.patch.dict(
    "os.environ",
    AIRFLOW_CONN_PULUMI_DEFAULT="pulumi://:pul-token@/?extra__pulumi__project_name=my-project&extra__pulumi__stack_name=dev&extra__pulumi__config_passphrase=pass",
)
class TestPulumiHook(unittest.TestCase):
    """
    Test Pulumi Hook.
    """

    def test_get_conn(self):
        # Instantiate hook
        hook = PulumiHook(
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


if __name__ == "__main__":
    unittest.main()
