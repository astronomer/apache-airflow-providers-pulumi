"""
Unittest module to test Operators.

Requires the unittest, pytest, and requests-mock Python libraries.

Run test:

    python3 -m unittest tests.operators.test_sample_operator.TestSampleOperator

"""
import logging
import os
import shutil
import unittest
import urllib.parse
from unittest import mock

# Import Operator
from airflow_provider_pulumi.operators.base import BasePulumiOperator
from airflow_provider_pulumi.operators.destroy import PulumiDestroyOperator
from airflow_provider_pulumi.operators.preview import PulumiPreviewOperator
from airflow_provider_pulumi.operators.up import PulumiUpOperator
from pulumi.automation import DestroyResult, PreviewResult, UpResult

log = logging.getLogger(__name__)

TESTS_PATH = os.path.join(os.path.dirname(__file__), os.pardir)


def random_resources():
    import pulumi
    import pulumi_random as random

    rand_int = random.RandomInteger("rand_int", seed="pytest", min=1, max=10)
    rand_string = random.RandomString("rand_string", length=10)

    pulumi.export("rand_int", rand_int.result)
    pulumi.export("rand_pet", rand_string.result)


# Mock the `conn_sample` Airflow connection
@mock.patch.dict(
    "os.environ",
    AIRFLOW_CONN_PULUMI_DEFAULT=f"pulumi://file%3A%2F%2F{urllib.parse.quote_plus(TESTS_PATH)}/?extra__pulumi__project_name=my-project&extra__pulumi__stack_name=dev&extra__pulumi__config_passphrase=pass",
)
class TestPulumiOperator(unittest.TestCase):
    """
    Test Pulumi Operator.
    """

    def setUp(self):
        self.base_operator = BasePulumiOperator(
            task_id="base_operator",
            pulumi_program=random_resources,
            pulumi_conn_id="pulumi_default",
            stack_config={"pytest": "true"},
        )

        self.preview_operator = PulumiPreviewOperator(
            task_id="preview_operator",
            pulumi_program=random_resources,
            pulumi_conn_id="pulumi_default",
            stack_config={"pytest": "true"},
        )

        self.up_operator = PulumiUpOperator(
            task_id="up_operator",
            pulumi_program=random_resources,
            pulumi_conn_id="pulumi_default",
            stack_config={"pytest": "true"},
        )

        self.destroy_operator = PulumiDestroyOperator(
            task_id="detroy_operator",
            pulumi_program=random_resources,
            pulumi_conn_id="pulumi_default",
            stack_config={"pytest": "true"},
        )
        return super().setUp()

    def test_base_operator(self):
        self.base_operator.pre_execute(context={})
        assert self.base_operator.stack.get_config("pytest").value == "true"

    def test_preview(self):
        self.preview_operator.pre_execute(context={})
        result: PreviewResult = self.preview_operator.execute(context={})

        assert result.change_summary.get("create") == 3

    def test_resource_create(self):
        # Airflow calls the operator's pre_execute method at runtime with the task run's bespoke context dictionary
        self.up_operator.pre_execute(context={})
        result: UpResult = self.up_operator.execute(context={})

        assert self.up_operator.stack.get_config("pytest").value == "true"
        assert result.outputs.get("rand_int").value == 10
        assert len(result.outputs.get("rand_pet").value) == 10
        assert result.summary.resource_changes.get("create") == 3

    def test_resource_destroy(self):
        self.up_operator.pre_execute(context={})
        self.up_operator.execute(context={})

        # Airflow calls the operator's pre_execute method at runtime with the task run's bespoke context dictionary
        self.destroy_operator.pre_execute(context={})
        result: DestroyResult = self.destroy_operator.execute(context={})

        assert result.summary.resource_changes.get("delete") == 3

    def tearDown(self) -> None:
        shutil.rmtree(os.path.join(TESTS_PATH, ".pulumi"))
        return super().tearDown()


if __name__ == "__main__":
    unittest.main()
