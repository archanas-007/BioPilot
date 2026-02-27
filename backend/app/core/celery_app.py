from celery import Celery

celery_app = Celery(
    "biopilot",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.worker.tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    task_time_limit=3600,
    task_soft_time_limit=3000,
    broker_connection_retry_on_startup=True
)

if __name__ == "__main__":
    celery_app.start()
