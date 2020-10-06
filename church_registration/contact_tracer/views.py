from django.shortcuts import render, redirect
from .models import Person
from .forms import PersonForm
from django.contrib import messages
from django.db.models import Q
from datetime import date
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import datetime, calendar
import qrcode
import os
import urllib
import re
from django.http import HttpResponse


def valid_name(s):
    r = re.compile("^[a-zA-Z\s\-\.]+$")
    if not r.search(s) is None:
        return True
    return False

def clean_qr_data(data):
    data['contact'] = data['contact'] if data['contact'] is not None else ''

def make_qr(data):
    # site = str(os.environ.get('WEB_URL'))
    site = "127.0.0.1"
    site = "http://" + site + "/"
    clean_qr_data(data)

    params = urllib.parse.urlencode(data)
    full_data = site + '?' + params

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=30,
        border=1,
    )
    qr.add_data(full_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

def registration(request):
    context = {}

    if request.method == 'GET' and 'name' in request.GET \
        and 'contact' in request.GET and 'address' in request.GET:
        name = request.GET.get('name', None)
        contact = request.GET.get('contact', None)
        address = request.GET.get('address', None)

        context = {
            'name': name if name is not None else '',
            'contact': contact if contact is not None else '',
            'address': address if address is not None else '',
            'pre_reg': True
        }

    return render(request, 'registration.html', context=context)


def qr_generator(request):
    return render(request, 'qr_generator.html', {})


def is_valid(data):
    name = data['name']
    contact = data['contact']
    address = data['address']
    msg = 'Successfully generated QR code! '
    result = True

    if name is None or address is None:
        result = False
        msg = 'Please fill up name and address!'
    
    elif len(name) == 0 or len(address) == 0:
        result =  False
        msg = 'Please fill up name and address!'

    # elif not valid_name(name):
    #     result =  False
    #     msg = 'Name should not have special characters (except dot and dash)!'

    elif contact is not None and len(contact) > 11:
        result =  False
        msg = 'Contact num should be less than 11!'
    
    else:
        return result, msg

def generate(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        contact = request.POST.get('contact', None)
        address = request.POST.get('address', None)

        # today = datetime.date.today()
        # next_sunday = today + datetime.timedelta( (calendar.SUNDAY - today.weekday()) % 7 )
        # next_sunday = next_sunday.strftime("%Y-%m-%d")
	
        data = {
            'name': name,
            'contact': contact,
            'address': address
            # 'date': next_sunday
        }

        validity, msg = is_valid(data)
        if validity:
            qr_code_img = make_qr(data)
            messages.add_message(
                    request,  messages.SUCCESS,
                    msg)
            response = HttpResponse(content_type='image/png')
            qr_code_img.save(response, "PNG")
            fname = re.sub(r'\W+', '', name)
            fname = fname.lower()
            response['Content-Disposition'] = "attachment; filename={}.png".format(fname)
            return response

        else:
            messages.add_message(
                request,  messages.WARNING,
                "There's a problem registering. " + msg)

    return redirect('/qr_generator')

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
    ).order_by("id").distinct()

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