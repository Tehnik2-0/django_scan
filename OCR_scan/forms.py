from .models import Download, Scan, DateBuilding, Task
from django.forms import ModelForm, FileField, ClearableFileInput, MultipleChoiceField, CheckboxInput


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DownloadForm(ModelForm):
    file = MultipleFileField()

    class Meta:
        model = Download
        fields = ['object_builbing', 'file', 'date_building']
