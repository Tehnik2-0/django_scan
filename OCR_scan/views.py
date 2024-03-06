from django.db import transaction
from django.shortcuts import redirect
from django.views.generic import FormView, ListView, CreateView

from .forms import DownloadForm
from .models import Scan, Download, Task, ObjectBuilbing, DateBuilding
from .tasks import recognition_scan


class NewHtml(ListView):
    model = Task
    template_name = 'NewSearch.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        tasks = Task.objects.all().order_by('-date')
        context['object_list'] = []
        for task in tasks:
            count = 0
            files = []
            scans = Scan.objects.filter(file__task=task)
            for s in scans:
                count_files = 0
                if s.cover:
                    cover = s.cover.url
                else:
                    cover = ''
                files.append({'title': s.file.file.name,
                              'file': s.file.file.url,
                              'cover': cover,
                              'text': s.text,
                              'object_builbing': s.file.object_builbing
                              })
            context['object_list'].append({'task_id': task.pk,
                                           'len_files': task.len_files,
                                           'date': task.date,
                                           'progress': task.progress,
                                           'scans': files
                                           })

        return context

class DownloadCreate(FormView):
    # Модель куда выполняется сохранение
    model = Download
    # Класс на основе которого будет валидация полей
    form_class = DownloadForm
    # Шаблон с помощью которого
    # будут выводиться данные
    template_name = 'download_create.html'
    # На какую страницу будет перенаправление
    # в случае успешного сохранения формы
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tasks'] = Task.objects.all().order_by('-date')
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        files = form.cleaned_data['file']
        object_builbing = form.cleaned_data['object_builbing']
        date_building = form.cleaned_data['date_building']
        task = Task(len_files=len(files), progress=0)
        task.save()
        for f in files:
            obj = self.model.objects.create(file=f, object_builbing=object_builbing, task=task,
                                            date_building=date_building)
        with transaction.atomic():
            recognition_scan.delay(task.pk)
        return redirect(self.get_success_url())


class SearchResultsView(ListView):
    model = Scan
    template_name = 'search.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['object_building'] = ObjectBuilbing.objects.all()
        context['date_building'] = DateBuilding.objects.all()
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_building = self.request.GET.get('object_building')
        date_building = self.request.GET.get('date_building')
        task_id = self.request.GET.get('task_id')
        if query is not None:
            object_list = Scan.objects.all()
            if object_building != '__all__':
                object_list = object_list.filter(file__object_builbing__name=object_building)
            if date_building != '__all__':
                object_list = object_list.filter(file__date_building__date=date_building)
            if task_id:
                object_list = object_list.filter(file__task__pk=task_id)
            if query:
                object_list = Scan.objects.filter(text__icontains=query)
            return object_list


class HomeView(ListView):
    model = Task
    template_name = 'home_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        tasks = Task.objects.all().order_by('-date')
        context['object_list'] = []
        for task in tasks:
            count = 0
            files = []
            scans = Scan.objects.filter(file__task=task)
            for s in scans:
                count_files = 0
                if s.cover:
                    cover = s.cover.url
                else:
                    cover = ''
                files.append({'title': s.file.file.name,
                              'file': s.file.file.url,
                              'cover': cover,
                              'text': s.text,
                              'object_builbing': s.file.object_builbing
                              })
            context['object_list'].append({'task_id': task.pk,
                                           'len_files': task.len_files,
                                           'date': task.date,
                                           'progress': task.progress,
                                           'scans': files
                                           })

        return context
