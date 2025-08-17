from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import *
import random
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .forms import PasswordResetRequestForm, SetNewPasswordForm
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator as token_generator
import random


token_generator = PasswordResetTokenGenerator()


def home(request):
    offers = Book.objects.order_by('?')[:3]
    return render(request, 'blog/home.html', {'offers': offers})


def list_book(request):
    all_book = Book.objects.all()
    paginator = Paginator(all_book, 3)
    num_paginator = request.GET.get('page', 1)
    try:
        all_book = paginator.page(num_paginator)
    except EmptyPage:
        all_book = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        all_book = paginator.page(1)
    return render(request, 'blog/list_book.html', {'all_book': all_book})


def detail_book(request, id):
    book = get_object_or_404(Book, id=id)
    form = CommentForm()
    comment = book.comments.filter(active=True)
    context = {
        'book': book,
        'form': form,
        'comment': comment
    }
    return render(request, 'blog/detail_book.html', context)


def ticket(request):
    if request.method == "POST":
        form = TicketForms(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Ticket.objects.create()
            ticket_obj.name = cd["name"]
            ticket_obj.family = cd["family"]
            ticket_obj.massage = cd["massage"]
            ticket_obj.email = cd["email"]
            ticket_obj.subject = cd["subject"]
            ticket_obj.save()
            return redirect('blog:home')
    else:
        form = TicketForms()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def comment_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.book = book
        comment.save()
    context = {
        'book': book,
        'comment': comment,
        'form': form
    }
    return render(request, 'forms/comment.html', context)


def search(request):
    query = None
    result = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result = result = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
    context = {
        'query': query,
        'result': result,
    }
    return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'email': user.email,
        'last_name': user.last_name,
        'first_name': user.first_name,
        'last_login': user.last_login,
        'date_joined': user.date_joined

    }
    return render(request, 'blog/profile.html', context)


def about_project(request):
    return render(request, 'blog/about.html')


def project_help(request):
    return render(request, 'blog/Help.html')


def terms_of_use(request):
    return render(request, 'blog/terms.html')


@login_required
def my_library(request):
    books = DownloadedBook.objects.filter(user=request.user).select_related('book')
    return render(request, 'forms/my_books.html', {'books': books})


@login_required
def download_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    from .models import DownloadedBook
    DownloadedBook.objects.get_or_create(user=request.user, book=book)
    if book.file and os.path.exists(book.file.path):
        return FileResponse(open(book.file.path, 'rb'), as_attachment=True)
    else:
        raise Http404("File not found")


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('blog:profile')
                else:
                    return HttpResponse("Your account is disabled")
            else:
                return HttpResponse("You are not logged in")
    else:
        form = LoginForm()
    return render(request, 'forms/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('blog:home')


def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                reset_path = reverse('blog:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                reset_url = request.build_absolute_uri(reset_path)
                send_mail(
                    'Password Reset',
                    f'Click here to reset your password: {reset_url}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
            return redirect('blog:password_reset_done')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'partials/password_reset_form.html', {'form': form})


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    validlink = False
    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                return redirect('blog:password_reset_complete')
        else:
            form = SetNewPasswordForm()
        return render(request, 'partials/password_reset_confirm.html', {'form': form, 'validlink': validlink})
    else:
        return render(request, 'partials/password_reset_confirm.html', {'validlink': validlink})


def password_reset_done_view(request):
    return render(request, 'partials/password_reset_done.html')


def password_reset_complete_view(request):
    return render(request, 'partials/password_reset_complete.html')


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'partials/congratulations.html', {'user': user})
    else:
        form = UserRegister()
    return render(request, 'partials/register.html', {'form': form})


def user_edit(request):
    try:
        account = request.user.account
    except ObjectDoesNotExist:
        account = Account.objects.create(user=request.user)

    if request.method == "POST":
        form = UserEdit(request.POST, instance=request.user)
        account_form = AccountEdit(request.POST, request.FILES, instance=account)
        if form.is_valid() and account_form.is_valid():
            form.save()
            account_form.save()
            return redirect('/')

    else:
        form = UserEdit(instance=request.user)
        account_form = AccountEdit(instance=account)

    context = {
        'user_form': form,
        'account_form': account_form,
        'account': account,
    }
    return render(request, 'partials/edit_information.html', context)