from django import forms
from .models import Newsletter


class ContactForm(forms.Form):
    # from_email = forms.EmailField(required=True)
    # subject = forms.CharField(required=True)
    # message = forms.CharField(widget=forms.Textarea, required=True)

    Email = forms.EmailField(required=True)
    # Password = forms.CharField( widget=forms.PasswordInput)
    Subject = forms.CharField(required=True)
    Message = forms.CharField(required=True)

    # widget = forms.Textarea

    def clean_Email(self):
        Email = self.cleaned_data['Email']
        return Email

    # def clean_Password(self):
    #     Password = self.cleaned_data['Password']
    #     return Password

    def clean_Subject(self):
        Subject = self.cleaned_data['Subject']
        return Subject

    def clean_Message(self):
        Message = self.cleaned_data['Message']
        return Message


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["email"]
