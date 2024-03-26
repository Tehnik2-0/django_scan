import functools
# python -m celery -A djangoProject worker -l info -P solo
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.db import transaction
from django.db.models import F
from django.db.transaction import atomic

from OCR_scan.models import Task, Download, Scan
from djangoProject.celery import app
from djangoProject.settings import PROJECT_ROOT, MEDIA_ROOT
from main import start


class custom_celery_task:
    """
    This is a decorator we can use to add custom logic to our Celery task
    such as retry or database transaction
    """
    def __init__(self, *args, **kwargs):
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                with transaction.atomic():
                    return func(*args, **kwargs)
            except Exception as e:
                # task_func.request.retries
                raise task_func.retry(exc=e, countdown=5)

        task_func = shared_task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func


@custom_celery_task(max_retries=5)
def add_db_task(id_task, count):
    Task.objects.filter(id=id_task).update(progress=count)


@app.task(bind=True)
def recognition_scan(self, id_task):
    files = Download.objects.filter(task=id_task)
    count = 0
    progress_recorder = ProgressRecorder(self)
    for file in files:
        name_image = file.file.name

        url = 'images' + '\\' + name_image[5:-3] + 'png'
        text = start(pdf_path=file.file.path, name_image=name_image)
        s = Scan.objects.create(title=file.file.name, file=file, text=text, cover=url)
        s.save()
        progress_recorder.set_progress(count, len(files))
        count += 1
