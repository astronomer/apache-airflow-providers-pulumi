import json
from typing import Any, Callable, Dict, Optional

from airflow.models.baseoperator import BaseOperator
from airflow.utils.context import Context
from airflow_provider_pulumi.hooks.automation import PulumiAutoHook
from pulumi import automation as auto


class BasePulumiOperator(BaseOperator):
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

    def pre_execute(self, context: Any):
        self.stack = self.hook.get_conn()
        for plugin, version in self.plugins.items():
            self.stack.workspace.install_plugin(plugin, version)

        for key, value in self.stack_config.items():
            self.stack.set_config(key, auto.ConfigValue(value))
        return super().pre_execute(context)
