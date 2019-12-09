from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import *


# Create your views here.


# def home(request):
#     return render(request,'home.html')
def register(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email already exists")
                return redirect('/')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "username already taken")
                return redirect('/')
            else:
                user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email,
                                                password=password1, username=username)
                user.save()
                messages.info(request, "user created successfully")
                return redirect('/')
        else:
            messages.info(request, "password not matching")
            return redirect('/')
    else:
        return render('home.html')

def home(request):
    if request.user.is_authenticated:
       return redirect('mainpage')
    else:
        return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('mainpage')
        else:
            messages.info(request, "username or password incorrect")
            return redirect('login')
    else:
        return render(request,'home.html')

    # else:
    #     return render(request,'home.html')


def logout(request):
    auth.logout(request)
    return render(request,'home.html')


def mainpage(request):
    current_movies = Movie.objects.all()
    return render(request, 'main_page.html', {'movies': current_movies})


def book_ticket(request, movie_id=None):
    # try:
    #     movie = Movie.objects.get(pk=movie_id)
    # except Movie.DoesNotExist:
    #     return HttpResponseNotFound('<h1>This movie does not exist</h1>')

    row = request.POST['ticket']
    ticket_num = row
    try:
        f = Ticket.objects.create(ticket_num=ticket_num, movie_id=movie_id)
        # f.save()
    except IntegrityError:
        print("ticket already reserved")

    return redirect('movie',movie_id=movie_id)


def movie_detail(request, movie_id=None):
    movie = Movie.objects.get(pk=movie_id)
    tickets = Ticket.objects.filter(movie=movie)
    ran = range(1, movie.tot_tickets + 1)
    l=Ticket.objects.filter(movie=movie, status=2).values_list('ticket_num', flat=True)
    rang=[]
    # for e in tickets:
    #     v=e.ticket_num
    #     l.append(v)
    for i in ran:
        rang.append(i)
    number_booked_tickets = tickets.count()
    available=movie.tot_tickets-number_booked_tickets
    context = {
        'list':l,
        'movie': movie,
        'tickets': tickets,
        'ran': ran,
        'number_booked_tickets':number_booked_tickets,
        'available':available,
    }
    return render(request, "movie.html", context)

def booked(already):
    l=[]
    for e in already:
        v=e.ticket_num
        l.append(v)
    return l
