from django.shortcuts import render, redirect
from .models import Person
from .forms import PersonForm
from django.contrib import messages
from django.db.models import Q
from datetime import date
from django.core.paginator import Paginator, EmptyPage, InvalidPage


def registration(request):
    return render(request, 'registration.html', {})


def register(request):
    is_success = "fail"
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    "Successful registration!")
            except:
                messages.add_message(
                    request,  messages.WARNING,
                    "There's a problem registering. Please try again!")
        else:
            messages.add_message(
                    request, messages.WARNING,
                    "There's a problem registering. Please try again!")
    else:
        form = PersonForm()

    return redirect('/')


def dashboard(request):
    today = date.today()
    people = Person.objects.filter(
        date__year=today.year, 
        date__month=today.month, 
        date__day=today.day
    ).order_by("id")

    PAGE_LIMIT = 10
    count_of_people = len(people)
    paginator = Paginator(people, PAGE_LIMIT)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        page_members = paginator.page(page)
    except(EmptyPage, InvalidPage):
        page_members = paginator.page(paginator.num_pages)

    context = {
        'persons': page_members,
        'count_of_people': count_of_people
    }

    return render(request, 'dashboard.html', context=context)