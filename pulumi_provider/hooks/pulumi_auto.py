import os
from typing import Callable, Optional
from urllib.parse import parse_qsl, urlencode

from airflow.hooks.base import BaseHook
from pulumi import automation as auto


class PulumiHook(BaseHook):
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
        project_name: str,
        stack_name: str,
        pulumi_program: Callable,
        pulumi_conn_id: str = default_conn_name,
    ) -> None:
        super().__init__()
        self.project_name = project_name
        self.stack_name = stack_name
        self.pulumi_program = pulumi_program
        self.pulumi_conn_id = pulumi_conn_id
        self.backend_url = None

    def get_conn(
        self,
    ) -> auto.Stack:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        if self.pulumi_conn_id:
            conn = self.get_connection(self.pulumi_conn_id)

            if conn.host and "://" in conn.host:
                self.backend_url = conn.host
            else:
                # schema defaults to HTTP
                schema = conn.schema if conn.schema else "https"
                host = conn.host if conn.host else "api.pulumi.com"
                self.backend_url = f"{schema}://{host}"

            if conn.port:
                self.backend_url = f"{self.backend_url}:{conn.port}"
            if conn.login:
                self.backend_url = f"{self.backend_url}/{conn.login}"
            if conn.password:
                os.environ["PULUMI_ACCESS_TOKEN"] = conn.password

            if conn.extra:
                try:
                    query: Optional[str] = urlencode(conn.extra_dejson)
                except TypeError:
                    query = None
                if query and conn.extra_dejson == dict(
                    parse_qsl(query, keep_blank_values=True)
                ):
                    self.backend_url += "?" + query

        stack = auto.create_or_select_stack(
            stack_name=self.stack_name,
            project_name=self.project_name,
            program=self.pulumi_program,
            opts=auto.LocalWorkspaceOptions(
                project_settings=auto.ProjectSettings(
                    name=self.project_name,
                    runtime="python",
                    backend=auto.ProjectBackend(url=self.backend_url),
                )
            ),
        )

        return stack
