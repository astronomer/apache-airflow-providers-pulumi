import json
from typing import Any

from airflow.utils.context import Context
from airflow_provider_pulumi.operators.base import BasePulumiOperator


class PulumiUpOperator(BasePulumiOperator):
    def execute(self, context: Context) -> Any:
        result = self.stack.up(on_output=self.log.info)
        self.log.info(
            f"update summary: \n{json.dumps(result.summary.resource_changes, indent=4)}"
        )
        return result.summary.resource_changes
