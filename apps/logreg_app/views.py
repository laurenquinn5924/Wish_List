# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Add_item


def index(request):
    return render(request, 'logreg_app/index.html')

def register(request):
    errors = User.objects.registration_validation(request.POST)
    if len(errors): #there are errors
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        person = User.objects.create(
        name = request.POST['name'],
        alias = request.POST['alias'],
        password = request.POST['password'],
        email_address = request.POST['email'])
        request.session['name'] = request.POST['name']
        request.session['id'] = person.id
        return redirect ('/display')

def login(request):
    errors = User.objects.user_validation(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        logged_in_user = User.objects.get(email_address=request.POST['email'])
        print logged_in_user
        request.session['name'] = logged_in_user.name
        request.session['id'] = logged_in_user.id
        return redirect ('/display')

def display(request):
    context = {
        'users' :User.objects.all(),
        'wishes' : Add_item.objects.filter(copied_by=User.objects.get(id=request.session['id'])),
        'other_wishes' : Add_item.objects.exclude(copied_by=User.objects.get(id=request.session['id']))
    }
    return render(request, 'logreg_app/display.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def new(request):
    return render(request, 'logreg_app/add_item.html')

def create(request):
    if request.method == 'POST':
        errors = Add_item.objects.wish_validation(request.POST)
        if (errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/new')
        else:
            user= User.objects.get(id=request.session['id'])
            wish = Add_item.objects.create(item=request.POST['item'],added_by=user, created_by=user)
            wish.copied_by.add(user)
            wish.save()
            return redirect('/display')
    else:
        return redirect('/display')


def join(request, wish_id):
    user = User.objects.get(id=request.session['id'])
    wish = Add_item.objects.get(id=wish_id)
    wish.copied_by.add(user)
    wish.save()
    return redirect('/display')


def leave(request, wish_id):
    user = User.objects.get(id=request.session['id'])
    wish = Add_item.objects.get(id=wish_id)
    wish.copied_by.remove(user)
    wish.save()
    return redirect('/display')


def info(request, wish_id):
    wish = Add_item.objects.get(id=wish_id)
    context = {
        'wish': wish,
        'other_wishes': User.objects.exclude(created_wishes__created_by=wish.created_by)
    }
    return render(request, 'logreg_app/item_info.html', context)



