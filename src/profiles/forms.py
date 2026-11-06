from django import forms

from .models import Configuration, Audience, Billing, MARKETING_OBJECTIVE_CHOICES

class ConfigurationForm(forms.ModelForm):
    number              = forms.IntegerField(min_value=0, max_value=50, required=True, localize=False, widget=forms.NumberInput(attrs={'type':'range'}))
    marketing_objective = forms.ChoiceField(label='Marketing objective', widget=forms.RadioSelect(), choices=MARKETING_OBJECTIVE_CHOICES)

    class Meta:
        model = Configuration
        exclude = ['ad_pk', 'access_token', 'updated', 'timestamp', 'submitted']

    
    def __init__(self, *args, **kwargs):
        super(ConfigurationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control '
        self.fields['marketing_objective'].widget.attrs['class'] += 'custom-control-input'
        self.fields['number'].widget.attrs['class'] += 'slider'

class AudienceForm(forms.ModelForm):

    class Meta:
        model = Audience
        exclude = ['ad_pk', 'updated', 'timestamp', 'submitted']

    def __init__(self, *args, **kwargs):
        super(AudienceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BillingForm(forms.ModelForm):

    class Meta:
        model = Billing
        exclude = ['ad_pk', 'updated', 'timestamp']

    def __init__(self, *args, **kwargs):
        super(BillingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'