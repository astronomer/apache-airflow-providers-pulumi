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
