from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email")

    def clean(self):
        email = self.cleaned_data.get('username')
        try:
            user = User.objects.get(email=email)
            self.cleaned_data['username'] = user.username  # replace email with actual username for authentication
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid login credentials")
        return super().clean()
