from app.core.celery_app import celery_app
import time

@celery_app.task(acks_late=True)
def sample_task(word: str) -> str:
    for i in range(1, 11):
        print(f"Task processing... {word} {i}/10")
        time.sleep(1)
    return f"Sample task complete: {word}"
