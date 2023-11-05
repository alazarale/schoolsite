from django import forms
from .models import GradeExcel


class GradeExcelForm(forms.ModelForm):
    class Meta:
        model = GradeExcel
        fields = ['file']
        labels = {'file': 'Choose excel containing grade lists'},

    def __init__(self, *args, **kwargs):
        super(GradeExcelForm, self).__init__(*args, **kwargs)


class StudentExcelForm(forms.Form):
    file = forms.FileField()



class SubjectExcelForm(forms.Form):
    file = forms.FileField()