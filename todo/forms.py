from django import forms

class TodoForm(forms.Form):
    text = forms.CharField(label='What to do?', max_length=255)

class TodoDeleteForm(forms.Form):
    pass

class TodoToggleStatusForm(forms.Form):
    pass