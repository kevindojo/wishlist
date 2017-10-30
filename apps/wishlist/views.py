from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.contrib.messages import error


# Create your views here.

def index(request):
    return render(request,'wishlist/index.html')


def create(request):
    errors= User.objects.validate_registration(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user = User.objects.valid_user(request.POST)
        request.session['user_id'] = user.id
        #keeps track of the current user_id that is "logged in", 
        # you can directly use it as argument, no need to pass into parameters: def example(x,y):
        messages.success(request, "registered")
        return redirect ('/success')






def login(request):
    errors= User.objects.validate_login(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/')
    else:
        user = User.objects.valid_login(request.POST)
        request.session['user_id'] = user.id
        messages.success(request, "Logged in")
        return redirect('/success')



def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'wishlist/success.html', context)




def logout(request):
    context = {
        'logout': request.session.pop('user_id')
    }
    return render(request,'wishlist/index.html', context)

################  END END LOGIN END END  ################################################################################


    # my_wish = models.ForeignKey(User, related_name = 'user_wish')
    # friend = models.ManyToManyField(User, related_name = 'friend_wish') 


def home(request):

    context = {
        'user': User.objects.get(id = request.session['user_id']),
        'user_products': Product.objects.filter(friend=request.session['user_id']),
        'friend_products': Product.objects.exclude(friend=request.session['user_id']),
        'user_delete': Product.objects.filter(my_wish_id = request.session['user_id']),
    }
    return render(request, 'wishlist/home.html', context)




def add_item(request):
    return render(request, 'wishlist/create.html')


def detail(request, id):

    context = {
        'item': Product.objects.get(id=id),
    }
    return render(request, 'wishlist/detail.html', context)


def create_item(request):
    current_user = User.objects.get(id = request.session['user_id'])
    new_product = Product.objects.create(item_name = request.POST['item_name'], my_wish = current_user)
    current_user.user_wish.add(new_product)
    #Fkey rn
    current_user.friend_wish.add(new_product)
    #M2M rn
    return redirect('/home')





def add_list(request, id):
    print 'poooop_list'
    items = Product.objects.get(id = id)
    user = User.objects.get(id = request.session['user_id'])

    user.friend_wish.add(items)
    #M2M rn
    return redirect('/home')



def remove_list(request,id):
    items = Product.objects.get(id = id)
    user = User.objects.get(id = request.session['user_id'])

    user.friend_wish.remove(items)
    #M2M rn
    return redirect('/home')


    

def delete(request, product_id):
    Product.objects.filter(my_wish_id = request.session['user_id'], id = product_id).delete()
    # my_wish = request.session = ['user_id'].delete()

    # items = Products.objects.get(id = id)

    # items.delete()
    return redirect('/home')
