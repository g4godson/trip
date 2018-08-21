from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):

    return render(request, 'index.html')

def register(request):
    # if User.objects.filter(email = request.POST['email']):
    #     return redirect('/')
    msgs = User.objects.regValidator(request.POST)
    if msgs:
        print(msgs)
        for key,values in msgs.items():
            print("value : ",values,"key",key)
            messages.error(request, values, extra_tags = key)



        return redirect('/')
    else :
        password = request.POST['password']
        hashedpw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashedpw)
        request.session['logged_in'] = user.id
        request.session['status'] = "Registered"
        return redirect('/home')

def login(request):
    msgs = User.objects.loginValidator(request.POST)
    if msgs:
        for key,values in msgs.items():
            print("value : ",values,"key",key)
            messages.error(request, values, extra_tags = key)

        return redirect('/')

    else:
        users = User.objects.filter(email = request.POST['login_email'])
        request.session['logged_in'] = users[0].id
        request.session['status'] = "logged in"
        return redirect('/home')

def logout(request):
    if not request.session['logged_in']:
        return redirect('/')
    request.session.clear()
    return redirect('/')

def home(request):
    if not request.session['logged_in']:
        return redirect('/')
    user = User.objects.get(id = request.session['logged_in'])
    user_trips = Trip.objects.filter(joined_users = user)
    print("user trips",user_trips)

    other_trips = Trip.objects.exclude(joined_users = user)
    print("other Trips", other_trips)
    return render(request, 'home.html', {'user' : user, 'user_trips' : user_trips, 'other_trips' : other_trips } )

def add(request):
    if not request.session['logged_in']:
        return redirect('/')



    return render(request, 'add.html')

def process(request):

    if not request.session['logged_in']:
        return redirect('/')
    print('inside add')
    msgs = Trip.objects.tripValidator(request.POST)

    if msgs:
        for key,values in msgs.items():
            print("value : ",values,"key",key)
            messages.error(request, values, extra_tags = key)


    else:
        user = User.objects.get(id = int(request.session['logged_in']))

        new =Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], start_date = request.POST['start_date'], end_date = request.POST['end_date'],  uploader = user)
        new.joined_users.add(user)

        print("Created new trip",new.destination)

    return redirect('/add')

def join(request,id):
    if not request.session['logged_in']:
        return redirect('/')

    user = User.objects.get(id = int(request.session['logged_in']))

    trip = Trip.objects.get(id = id)

    trip.joined_users.add(user)

    return redirect('/home')

def cancel(request,id):
    if not request.session['logged_in']:
        return redirect('/')

    user = User.objects.get(id = int(request.session['logged_in']))

    trip = Trip.objects.get(id = id)

    trip.joined_users.remove(user)

    return redirect('/home')

def delete(request,id):
    if not request.session['logged_in']:
        return redirect('/')
    trip = Trip.objects.get(id = id)

    trip.joined_users.clear()
    trip.delete()

    return redirect('/home')

def show(request,id):
    if not request.session['logged_in']:
        return redirect('/')
    trip = Trip.objects.get(id = id)
    print("@@@",trip.joined_users.all()[0].first_name)


    return render(request, 'show.html', {'trip' : trip, 'other_users' :  trip.joined_users.all() })
