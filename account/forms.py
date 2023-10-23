from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин',
    }))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль',
    }))


# class CommentForm(forms.ModelForm):
#     author = forms.CharField(label='Ваше имя:', widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Введите имя',
#     }))
#     text = forms.CharField(label='Комментарий:', widget=forms.Textarea(attrs={
#         'class': 'form-control',
#         'placeholder': 'Введите комментарий',
#     }))
#
#     class Meta:
#         model = Comment
#         fields = ('author', 'text')