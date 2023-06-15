from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "class": "form-control",
            "id": "username",
            "placeholder": "username...",
            "name": "username",
            "autocomplete": "off",
            "type": "text",
        })
        self.fields['password'].widget.attrs.update({
            "class": "form-control",
            "id": "password",
            "placeholder": "password...",
            "name": "password",
            "autocomplete": "off",
            "type": "password",
        })


class MyUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "username"
        })
        self.fields['password1'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "password"
        })
        self.fields['password2'].widget.attrs.update({
            "class": "form-control",
            "placeholder": "confirm password"
        })

