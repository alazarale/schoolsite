from django import forms
from .models import AccadamicYear
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset, HTML, Field, ButtonHolder


class AccadamicYearForm(forms.ModelForm):
    class Meta:
        model = AccadamicYear
        fields = ['name_EC']
        labels = {'name_EC': 'Academic Year(In E.C)'}
        widgets = {
            'name_EC': forms.TextInput(attrs={'placeholder': 'Year in E.C'}),
        }