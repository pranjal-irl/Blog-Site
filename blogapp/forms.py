from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExtendedSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    get_notified = forms.BooleanField(required=False, label="Get notified for new blogs")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.profile
            profile.get_notified = self.cleaned_data.get('get_notified', False)
            profile.save()
        return user