import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        label='Password2',
        error_messages={
            'required': 'Please, repeat your password'
        }
    )
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']
        labels = {
            'username': 'Digite o seu usuário.'
        }
        help_texts = {
            'e-mail': 'The e-mail must be valid.'
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
                'max_lenth': 'This field must have less than 3 character.'
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'username'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            })
        }

        def clean_password(self):
            data = self.cleaned_data.get('password')

            if 'atenção' in data:
                raise ValidationError(
                    'Não digite %(value)s no campo password',
                    code='invalid',
                    params={ 'value', 'atenção' }
                )
            
            return data
        
        def clean_first_name(self):
            data = self.cleaned_data.get('first_name')

            if 'John Doe' in data:
                raise ValidationError(
                    'Não digite %(value)s no campo password',
                    code='invalid',
                    params={ 'value', 'atenção' }
                )
            
            return data
        
        def clean(self):
            cleaned_data = super().clean()

            password = cleaned_data.get('password')
            password2 = cleaned_data.get('password2')

            if password != password2:
                password_confirmation_error = ValidationError(
                    'Password and password2 must be equal',
                    code='invalid'
                )
                raise ValidationError({
                    'password': password_confirmation_error,
                    'password2': [
                        password_confirmation_error,
                    ],
                })

