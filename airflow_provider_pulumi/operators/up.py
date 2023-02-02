import json
from typing import Any, Callable, Dict, Optional

from airflow.utils.context import Context
from airflow_provider_pulumi.hooks.automation import PulumiAutoHook
from airflow_provider_pulumi.operators.base import BasePulumiOperator


class PulumiUpOperator(BasePulumiOperator):
    """
    PulumiUpOperator creates infrastructure resources using the Pulumi Automation API.

    :param pulumi_program: the Pulumi program callable for creating infrastructure resources.
    :type pulumi_program: Callable
    :param stack_config: dictionary of configuration options for the Pulumi stack, defaults to None
        Example:
            stack_config={"aws:region": "us-west-2}
    :type stack_config: Optional[Dict[str, Any]], optional
    :param plugins: a dictionary of plugins to include in the Pulumi program, defaults to None
        Example:
            plugins={"aws": "v5.0.0}
    :type plugins: Optional[Dict[str, str]], optional
    :param pulumi_conn_id: connection that contains Pulumi stack backend URL, project name, stack
        name, and other required details about connecting with Pulumi, defaults to PulumiAutoHook.default_conn_name
    :type pulumi_conn_id: Optional[str], optional
    """

    def __init__(
        self,
        *args,
        pulumi_program: Callable,
        stack_config: Optional[Dict[str, Any]] = None,
        plugins: Optional[Dict[str, str]] = None,
        pulumi_conn_id: Optional[str] = PulumiAutoHook.default_conn_name,
        **kwargs,
    ):
        super().__init__(
            *args,
            pulumi_program=pulumi_program,
            stack_config=stack_config,
            plugins=plugins,
            pulumi_conn_id=pulumi_conn_id,
            **kwargs,
        )

    def execute(self, context: Context) -> Any:
        result = self.stack.up(on_output=self.log.info)
        self.log.info(
            f"update summary: \n{json.dumps(result.summary.resource_changes, indent=4)}"
        )
        return result.summary.resource_changes
