from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

from itertools import chain

# Create your views here.

def homePage(request):
	return render(request, 'mainpage.html')

def allQuestionPage(request, tag):
	questions = Question.objects.filter(tag=tag)
	polls = Poll.objects.filter(tag=tag)
	total = sorted(chain(questions, polls), key = lambda x: x.created_at, reverse = True)
	return render(request, 'home-page.html', {
		'questions': total,
		'tag': tag
	})

def allBlogPage(request, tag):
	blogs = Blog.objects.filter(tag=tag).order_by('-created_at')
	return render(request, 'blog-page.html', {
		'blogs': blogs,
		'tag': tag,
	})

def registerPage(request):
	if request.method == 'POST':
		try:
			form = RegisterUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				login(request, user)
				return redirect('index')
		except Exception as e:
			print(e)
			raise
	return render(request, 'register.html', {
		'form': RegisterUserForm()
	})

def loginPage(request):
	if request.method == 'POST':
		try:
			form = LoginForm(data=request.POST)
			if form.is_valid():
				user = form.get_user()
				login(request, user)
				return redirect('index')
		except Exception as e:
			print(e)
			raise
	return render(request, 'login.html', {
		'form': LoginForm()
	})

@login_required(login_url='register')
def logoutPage(request):
	logout(request)
	return redirect('login')

def blogPage(request, tag, id):
	response_form = NewBlogResponseForm()	
	if request.method == 'POST':
		try:
			response_form = NewBlogResponseForm(request.POST)
			if response_form.is_valid():
				response = response_form.save(commit=False)
				response.user = request.user
				response.blog = Blog(id=id)
				response.save()
				return redirect('blog', tag=tag, id=id)
		except Exception as e:
			print(e)
			raise
		
	blog = Blog.objects.get(id=id)
	return render(request, 'blog.html', {
		'blog': blog,
        'blog_response_form': response_form,
		'tag': tag,
	})

def questionPage(request, tag, id):
	response_form = NewResponseForm()
	reply_form = NewReplyForm()
	
	if request.method == 'POST':
		try:
			response_form = NewResponseForm(request.POST)
			if response_form.is_valid():
				response = response_form.save(commit=False)
				response.user = request.user
				response.question = Question(id=id)
				response.save()
				return redirect('question', tag= tag, id= id)
		except Exception as e:
			print(e)
			raise
		
	question = Question.objects.get(id=id)
	return render(request, 'question.html', {
		'question': question,
        'response_form': response_form,
		'reply_form': reply_form,
		'tag': tag,
	})

@login_required(login_url='register')
def newBlog(request, tag):
	if request.method == 'POST':
		try:
			form = NewBlogForm(request.POST)
			if form.is_valid():
				blog = form.save(commit=False)
				blog.author = request.user
				blog.tag = tag
				blog.save()
				return redirect('all-blog', tag=tag)
		except Exception as e:
			print(e)
			raise
	return render(request, 'new-blog.html', {
		'form': NewBlogForm()
	})

@login_required(login_url='register')
def newQuestion(request, tag):
	if request.method == 'POST':
		try:
			form = NewQuestionForm(request.POST)
			if form.is_valid():
				question = form.save(commit=False)
				question.author = request.user
				question.tag = tag
				question.save()
				return redirect('all-questions', tag=tag)
		except Exception as e:
			print(e)
			raise
	return render(request, 'new-question.html', {
		'form': NewQuestionForm(),
		'tag': tag
	})

@login_required(login_url='register')
def replyPage(request):
	if request.method == 'POST':
		try:
			form = NewReplyForm(request.POST)
			if form.is_valid():
				question_id = request.POST.get('question')
				parent_id = request.POST.get('parent')
				tag = request.POST.get('tag')
				reply = form.save(commit=False)
				reply.user = request.user
				reply.question = Question(id=question_id)
				reply.parent = Response(id=parent_id)
				reply.save()
				return redirect('question', id=question_id, tag=tag)
		except Exception as e:
			print(e)
			raise

	return redirect('index')

@login_required(login_url='register')
def newPollPage(request, tag):
	if request.method == 'POST':
		try:
			form = NewPollForm(request.POST)
			if form.is_valid():
				poll = form.save(commit=False)
				poll.author = request.user
				poll.tag = tag
				poll.save()
				id = poll.id
				choices = (form.cleaned_data['options']).split(',')
				makeChoices(choices, id)
				return redirect('all-questions', tag=tag)
		except Exception as e:
			print(e)
			raise
	return render(request, 'new-poll.html', {
		'form': NewPollForm(),
		'tag': tag
	})

def makeChoices(arr, id):
	try:
		p = Poll(id=id)
		for i in arr:
			c = Choice(poll=p, text=i)
			c.save()
	except Exception as e:
		print(e)
		raise

def pollPage(request, tag, id):
	poll = Poll.objects.get(id=id)
	options = poll.choices.all()
	submitted = Track.objects.filter(poll=poll, user=request.user).exists()
	if submitted:
		return redirect('poll-result', tag=tag, id=id)
	return render(request, 'poll.html', {
		'poll': poll,
		'options': options,
		'tag': tag,
	})

def pollPageResult(request, tag, id):
	poll = Poll.objects.get(id=id)
	options = poll.choices.all()
	if request.method == 'POST':
		try:
			inputvalue = request.POST.get('choice')
			if inputvalue:
				selected = options.get(id=inputvalue)
				submitted = Track.objects.filter(poll=poll, user=request.user).exists()
				if not submitted:
					selected.vote += 1
					selected.save()
					track = Track(poll=poll, user=request.user)
					track.save()
		except Exception as e:
			print(e)
			raise
	return render(request, 'poll-result.html', {
		'poll': poll,
		'results': calculatePollResult(options),
		'tag': tag,
	})

def calculatePollResult(options):
	total = 0
	for option in options:
		total += option.vote
	result = []
	for option in options:
		result.append((option.text, int((option.vote/total) * 100)))
	return result