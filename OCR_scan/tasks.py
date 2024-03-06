import functools
# python -m celery -A djangoProject worker -l info -P solo
from celery import shared_task
from django.db import transaction
from django.db.models import F
from django.db.transaction import atomic

from OCR_scan.models import Task, Download, Scan
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


@custom_celery_task(max_retries=5)
def add_db_scan(title, file, text, cover):
    s = Scan.objects.create(title=title, file=file, text=text, cover=cover)
    s.save()


@custom_celery_task(max_retries=5)
def recognition_scan(id_task):
    files = Download.objects.filter(task=id_task)
    count = 1
    for file in files:
        name_image = file.file.name

        url = 'images' + '\\' + name_image[5:-3] + 'png'
        text = start(pdf_path=file.file.path, name_image=name_image)
        add_db_scan(title=file.file.name, file=file, text=text, cover=url)
        add_db_task(id_task, count)
        count += 1
