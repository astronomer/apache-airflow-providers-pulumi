import os
from typing import Any, Callable, Dict

from airflow.hooks.base import BaseHook
from pulumi import automation as auto


class PulumiAutoHook(BaseHook):
    """
    Sample Hook that interacts with an HTTP endpoint the Python requests library.

    :param method: the API method to be called
    :type method: str
    :param pulumi_conn_id: connection that has the base API url i.e https://www.google.com/
        and optional authentication credentials. Default headers can also be specified in
        the Extra field in json format.
    :type pulumi_conn_id: str
    :param auth_type: The auth type for the service
    :type auth_type: AuthBase of python requests lib
    """

    conn_name_attr = "pulumi_conn_id"
    default_conn_name = "pulumi_default"
    conn_type = "pulumi"
    hook_name = "Pulumi"

    def __init__(
        self,
        pulumi_program: Callable,
        pulumi_conn_id: str = default_conn_name,
    ) -> None:
        super().__init__()
        self.pulumi_program = pulumi_program
        self.pulumi_conn_id = pulumi_conn_id
        self.backend_url = None
        self.project_name = None
        self.stack_name = None
        self.env_vars: Dict[str, str] = {
            k[8:]: v for k, v in os.environ.items() if k.startswith("PULUMI__")
        }

    @staticmethod
    def get_connection_form_widgets() -> Dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import (
            BS3PasswordFieldWidget,
            BS3TextFieldWidget,
        )
        from flask_babel import lazy_gettext
        from wtforms import StringField, validators

        return {
            "extra__pulumi__project_name": StringField(
                lazy_gettext("Project Name"),
                widget=BS3TextFieldWidget(),
                validators=[validators.data_required()],
            ),
            "extra__pulumi__stack_name": StringField(
                lazy_gettext("Stack Name"),
                widget=BS3TextFieldWidget(),
                validators=[validators.data_required()],
            ),
            "extra__pulumi__config_passphrase": StringField(
                lazy_gettext("Config Passphrase"),
                widget=BS3PasswordFieldWidget(),
            ),
        }

    @staticmethod
    def get_ui_field_behaviour() -> Dict[str, Any]:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ["schema", "login", "extra", "port"],
            "relabeling": {
                "host": "Backend URL",
                "password": "Access Token",
            },
            "placeholders": {
                "host": "pulumi backend url (leave blank for Pulumi Service backend)",
                "password": "pulumi access token",
                "extra__pulumi__project_name": "pulumi project name",
                "extra__pulumi__stack_name": "pulumi stack name",
                "extra__pulumi__config_passphrase": "config secrets passphrase",
            },
        }

    def get_conn(
        self,
    ) -> auto.Stack:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        conn = self.get_connection(self.pulumi_conn_id)

        self.project_name = conn.extra_dejson.get("extra__pulumi__project_name")
        self.stack_name = conn.extra_dejson.get("extra__pulumi__stack_name")

        self.backend_url = conn.host

        if conn.password:
            self.env_vars["PULUMI_ACCESS_TOKEN"] = conn.password

        config_passphrase = conn.extra_dejson.get("extra__pulumi__config_passphrase")
        if config_passphrase:
            self.env_vars["PULUMI_CONFIG_PASSPHRASE"] = config_passphrase

        stack_opts = auto.LocalWorkspaceOptions(
            env_vars=self.env_vars,
        )
        if self.backend_url:
            stack_opts.project_settings = auto.ProjectSettings(
                name=self.project_name,  # type: ignore
                runtime="python",
                backend=auto.ProjectBackend(url=self.backend_url),  # type: ignore
            )

        stack = auto.create_or_select_stack(
            stack_name=self.stack_name,  # type: ignore
            project_name=self.project_name,
            program=self.pulumi_program,
            opts=stack_opts,
        )

        return stack
