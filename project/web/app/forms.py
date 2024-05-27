from django import forms
from django.forms import ModelForm
from .models import Student
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User



class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            student = Student.objects.create(user=user, name=user.username, email=user.email)
        return user



class studentForm(ModelForm):
    class Meta: 
        model = Student
        fields="__all__"
        exclude=['user']