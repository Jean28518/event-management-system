from django import forms

class EmailForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    subject = forms.CharField(label='Subject', max_length=100, widget=forms.TextInput(attrs={'class': "form-control"}))
    answer_to_email = forms.CharField(label='Answer to email adress', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}))
    body = forms.CharField(label='Body', max_length=8192, widget=forms.Textarea(attrs={'class': "form-control"}))
