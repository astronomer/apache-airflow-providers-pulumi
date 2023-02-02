from typing import Any, Callable, Dict, Optional

from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from airflow_provider_pulumi.hooks.automation import PulumiAutoHook
from pulumi import automation as auto


class BasePulumiOperator(BaseOperator):
    """
    BasePulumiOperator contains common methods for interacting with a Pulumi stack
    via the provided pulumi_conn_id.

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
        super().__init__(*args, **kwargs)

        self.pulumi_program = pulumi_program
        self.stack_config = stack_config or {}
        self.plugins = plugins or {}
        self.pulumi_conn_id = pulumi_conn_id
        self.stack: auto.Stack = None
        self.hook = PulumiAutoHook(
            pulumi_program=self.pulumi_program,
            pulumi_conn_id=self.pulumi_conn_id,
        )

    def pre_execute(self, context: Context):
        """Sets up the provided stack config for the Pulumi stack and installs provided plugins."""
        self.stack = self.hook.get_conn()
        for plugin, version in self.plugins.items():
            self.stack.workspace.install_plugin(plugin, version)

        for key, value in self.stack_config.items():
            self.stack.set_config(key, auto.ConfigValue(value))
        super().pre_execute(context)
