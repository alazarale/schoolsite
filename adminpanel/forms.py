from decimal import MAX_EMAX
from django import forms
from acctype.models import Parent
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Button, Fieldset, HTML, Field, ButtonHolder


class ParentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = Parent
        fields = ['phone', 'job', 'address', 'relation_ship']
    
    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div('first_name', css_class="col-sm-6"),
                Div('last_name', css_class="col-sm-6"),
                css_class='row'
            ),
            Div(
                Div('phone', css_class="col-sm-6"),
                Div('job', css_class="col-sm-6"),
                css_class='row'
            ),
            Div(
                Div('address', css_class="col-sm-8"),
                css_class='row'
            ),
            Div(
                Div('relation_ship', css_class="col-sm-6"),
                css_class='row'
            ),
            
        )
