"""
Unittest module to test Operators.

Requires the unittest, pytest, and requests-mock Python libraries.

Run test:

    python3 -m unittest tests.operators.test_sample_operator.TestSampleOperator

"""
import logging
import unittest

# Import Operator
from airflow_provider_pulumi.operators.base import BasePulumiOperator
from airflow_provider_pulumi.operators.destroy import PulumiDestroyOperator
from airflow_provider_pulumi.operators.preview import PulumiPreviewOperator
from airflow_provider_pulumi.operators.up import PulumiUpOperator

log = logging.getLogger(__name__)


# # Mock the `conn_sample` Airflow connection
# @mock.patch.dict('os.environ', AIRFLOW_CONN_CONN_SAMPLE='http://https%3A%2F%2Fwww.httpbin.org%2F')
# class TestSampleOperator(unittest.TestCase):
#     """
#     Test Sample Operator.
#     """

#     @requests_mock.mock()
#     def test_operator(self, m):

#         # Mock endpoint
#         m.get('https://www.httpbin.org/', json={'data': 'mocked response'})

#         operator = SampleOperator(
#             task_id='run_operator',
#             sample_conn_id='conn_sample',
#             method='get'
#         )

#         # Airflow calls the operator's execute method at runtime with the task run's bespoke context dictionary
#         response_payload = operator.execute(context={})
#         response_payload_json = json.loads(response_payload)

#         log.info(response_payload_json)

#         # Assert the API call returns expected mocked payload
#         assert response_payload_json['data'] == 'mocked response'


if __name__ == "__main__":
    unittest.main()
