"""Collection of Cereal schedules"""

from dagster import schedule

from example.jobs import test


@schedule(
    cron_schedule="0 9 * * 1-5",
    job=test,
)
def every_weekday_9am(context):
    """Example of how to setup a weekday schedule for a job."""
    date = context.scheduled_execution_time.strftime("%Y-%m-%d")
    return {"ops": {"download_cereals": {"config": {"date": date}}}}
