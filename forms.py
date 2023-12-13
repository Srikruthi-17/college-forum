from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *
from django import forms

class RegisterUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		widgets = {
			'email': forms.EmailInput(attrs={
				'required': True,
				'placeholder': 'RollNumber@cmrcet.ac.in',
				'autofocus': True
			}),

			'username': forms.TextInput(attrs={
				'required': True,
				'placeholder': 'RollNumber',
			})
		}

	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)
		self.fields['password1'].widget.attrs = {'placeholder': 'password'}
		self.fields['password2'].widget.attrs = {'placeholder': 'confirm password'}

class LoginForm(AuthenticationForm):
	class Meta:
		fields = "__all__"

class NewQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'body']
		widgets = {
			'title': forms.TextInput(attrs={
				'autofocus': True,
				'placeholder': "Enter your question"
			})
		}

class NewResponseForm(forms.ModelForm):
	class Meta:
		model = Response
		fields = ['body']

class NewReplyForm(forms.ModelForm):
	class Meta:
		model = Response
		fields = ['body']
		widgets = {
			'body': forms.Textarea(attrs={
				'rows': 2,
				'placeholder': "what are your thoughts?",
			})
		}

class NewBlogForm(forms.ModelForm):
	class Meta:
		model = Blog
		fields = ['title', 'body']
		widgets = {
			'title': forms.TextInput(attrs={
				'autofocus': True,
				'placeholder': "Enter your blog Title",
			})
		}

class NewBlogResponseForm(forms.ModelForm):
	class Meta:
		model = BlogResponse
		fields = ['body']

class NewPollForm(forms.ModelForm):
	class Meta:
		model = Poll
		fields = ['title', 'options']
		widgets = {
			'title': forms.TextInput(attrs={
				'autofocus': True,
				'placeholder': "Enter your Poll Title",
			}),

			'options': forms.TextInput(attrs={
				'autofocus': True,
				'placeholder': "Enter your options sepreated using comma ',' ",
			})
		}