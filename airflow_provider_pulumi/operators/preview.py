import json
from typing import Any

from airflow.utils.context import Context
from airflow_provider_pulumi.operators.base import BasePulumiOperator


class PulumiPreviewOperator(BasePulumiOperator):
    def execute(self, context: Context) -> Any:
        result = self.stack.preview(on_output=self.log.info)
        self.log.info(
            f"preview summary: \n{json.dumps(result.change_summary, indent=4)}"
        )
        return result.change_summary
