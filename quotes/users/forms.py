from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput())
    email = forms.EmailField(max_length=254,
                            required=True,
                            widget=forms.EmailInput())
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = Profile
        fields = ['avatar']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Оновити імейл користувача
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
        return profile
    

class UserUpdateEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Користувач з таким email вже існує.")
        return email