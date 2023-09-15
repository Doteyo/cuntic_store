from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from store.forms import *
from .models import Cunty, Room, Message
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
import hashlib
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def generate_hash(data):
    # Create a new SHA256 hash object
    hasher = hashlib.sha256()

    # Convert the data to bytes
    data_bytes = data.encode('utf-8')

    # Update the hash object with the data bytes
    hasher.update(data_bytes)

    # Get the resulting hash code as a hexadecimal string
    hash_code = hasher.hexdigest()

    return hash_code


# Create your views here.
def home(req):
    if req.method == "POST":
        post_id = req.POST.get("post-id")
        buy_id = req.POST.get("buy-id")
        if post_id:
            post = Cunty.objects.filter(id=post_id).first()
            if post and req.user.has_perm("store.delete_cunty"):
                post.delete()
        if buy_id:
            return redirect(f'buy/{buy_id}')
    return render(req, "home.html", {"items": Cunty.objects.filter(seller=1), "status": ["Принят", "Отправлен"]})


@login_required(login_url="/login")
def buy(req, id):
    item = Cunty.objects.filter(id=id).first()
    return render(req, "buy.html", {"price": item.price, "size": item.size, "weight": item.weight, "sizes":
    {"2XS": 0,
             "XS": 1,
             "S": 2,
             "M": 3,
             "L": 4,
             "XL": 5,
             "XXL": 6,
             "XXXL": 7,
             "XXXXL": 8,
             "XXXXXL": 9,
             "XXXXXXXL": 10, }})


@login_required(login_url="/login")
def create_listing(req):
    if req.method == "POST":
        form = ListingForm(req.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = req.user
            item.size = item.size.upper()
            item.save()
            return redirect("/")
    else:
        form = ListingForm()
    return render(req, "create_listing.html", {"form": form})


def sign_up(req):
    if req.method == 'POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(req, 'registration/sign_up.html', {"form": form})


@login_required(login_url="/login")
def cart(req):
    if req.method == "POST":
        post_id = req.POST.get("post-id")
        based_id = req.POST.get("based-id")
        chat = req.POST.get("chat")
        if post_id:
            post = Cunty.objects.filter(id=post_id).first()
            if post and (post.seller == req.user or req.user.has_perm("store.delete_cunty")):
                post.delete()

        if based_id:
            based = Cunty.objects.filter(id=based_id).first()
            if based:
                based.status += 1
                based.save(update_fields=["status"])

        if chat:
            return redirect(f"room/{generate_hash(chat)}")

    if req.user.is_staff:
        return render(req, 'cart.html',
                      {"items": Cunty.objects.exclude(seller=req.user.id), "status": ["Принят", "Отправлен"]})
    return render(req, 'cart.html',
                  {"items": Cunty.objects.filter(seller=req.user.id), "status": ["Принят", "Отправлен"]})


@login_required(login_url="/login")
def room(request, room):
    username = request.user
    if not Room.objects.filter(name=room).exists():
        new_room = Room.objects.create(name=room)
        new_room.save()
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
