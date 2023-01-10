# Pulumi Airflow Provider


An airflow provider to:
- preview infrastructure resources before deployment
- deploy infrastructure resources via Pulumi
- destroy infrastructure resources

This package currently contains

1 hook :
- `airflow_provider_pulumi.hooks.automation.PulumiAutoHook` - a hook to setup the Pulumi backend connection.

4 operators :
- `airflow_provider_pulumi.operators.base.BasePulumiOperator` - the base operator for Pulumi.
- `airflow_provider_pulumi.operators.preview.PulumiPreviewOperator` - an operator that previews the deployment of infrastructure resources with Pulumi.
- `airflow_provider_pulumi.operators.up.PulumiUpOperator` - an operator that deploys infrastructure resources with Pulumi.
- `airflow_provider_pulumi.operators.destroy.PulumiDestroyOperator` - an operator that destroys infrastructure resources with Pulumi.

## Requirements
These operators require the Pulumi client to be installed. Use the following script to install the Pulumi client in your Airflow environment:

```bash
curl -fsSL https://get.pulumi.com | sh
export PATH="$HOME/.pulumi/bin:$PATH"
```

## Quick start

` pip install airflow-provider-pulumi`

```python
# example_pulumi_dag.py
from datetime import datetime

from airflow.decorators import dag
from airflow_provider_pulumi.operators.destroy import PulumiDestroyOperator
from airflow_provider_pulumi.operators.preview import PulumiPreviewOperator
from airflow_provider_pulumi.operators.up import PulumiUpOperator


@dag(
    schedule_interval=None,
    start_date=datetime(2022, 1, 1),
    tags=["example"],
)
def example_pulumi():
    def create_s3_bucket():
        import pulumi
        import pulumi_aws as aws

        # Creates an AWS resource (S3 Bucket)
        bucket = aws.s3.Bucket("my-bucket")

        # Exports the DNS name of the bucket
        pulumi.export("bucket_name", bucket.bucket_domain_name)

    preview_s3_create_task = PulumiPreviewOperator(
        task_id="preview_s3_create",
        pulumi_program=create_s3_bucket,
        stack_config={"aws:region": "us-west-2"},
        plugins={"aws": "v5.0.0"},
    )

    s3_create_task = PulumiUpOperator(
        task_id="s3_create",
        pulumi_program=create_s3_bucket,
        stack_config={"aws:region": "us-west-2"},
        plugins={"aws": "v5.0.0"},
    )

    s3_destroy_task = PulumiDestroyOperator(
        task_id="s3_destroy",
        pulumi_program=create_s3_bucket,
        stack_config={"aws:region": "us-west-2"},
        plugins={"aws": "v5.0.0"},
    )

    preview_s3_create_task >> s3_create_task >> s3_destroy_task


example_pulumi_dag = example_pulumi()
```

## Development

### Unit Tests

Unit tests are located at `tests`, the Pulumi client is required to run these tests. Execute with `pytest`.
