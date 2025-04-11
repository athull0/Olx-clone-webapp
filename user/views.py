from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from website.views import homepage
from .forms import RegUser,ProfileForm,AdForm,ContactForm
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse,HttpResponseForbidden
from django.contrib.auth.decorators import login_required


# Create your views here.
def adduser(request):
    if request.method == 'POST':
        form = RegUser(request.POST,request.FILES)
        if form.is_valid():
            a = form.save()
            Profile.objects.create(user = a)
            login(request,a)
            messages.success(request,'User has been registered')
            return redirect(homepage)
    else:

        form = RegUser()
    return render(request,'register.html',{'form':form})

def loginpage(request):
    if request.method == 'POST':
        usern = request.POST['user']
        passw = request.POST['pass']
        user = authenticate(request,username=usern,password=passw)
        if user:
            login(request,user)
            messages.success(request,'user has been authenticated')
            return redirect(homepage)
        else:
        
            messages.error(request,'Invalid username or password')
            return redirect(loginpage)
    
    return render(request,'login.html')

def logoutpage(request):
    logout(request)
    messages.success(request,'User has logged out')
    return redirect(homepage)

def profilepage(request):
    a = request.user
    pro = Profile.objects.get(user = a)
    return render(request,'profile.html',{'pro':pro})

def editprofile(request,eid):
    pro = get_object_or_404(Profile,pk = eid)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=pro)
        if form.is_valid():
            form.save()
            return redirect(homepage)
    else:

        form = ProfileForm(instance=pro)
    return render(request,'editprofile.html',{'form':form})

def addproducts(request):
    if request.method == 'POST':
        form = AdForm(request.POST,request.FILES)
        files = request.FILES.getlist('images')
        
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            for image in files:
                Adimage.objects.create(ad=ad,image=image)
            messages.success(request,'Product successfully added')
            return redirect(profilepage)
    else:
        form = AdForm()
    return render(request,'addpro.html',{'form':form})

def ad_list(request):
    ads = Ad.objects.filter(user = request.user)
    return render(request,'ad_list.html',{'ads':ads})

def adedit(request,aid):
    ads = Ad.objects.get(id = aid)
    files = request.FILES.getlist('images')

    if request.method == 'POST':
        form = AdForm(request.POST,request.FILES,instance=ads)
        if form.is_valid():
            ad=form.save()
            ad.save()
            for image in files:
                Adimage.objects.create(ad=ad,image=image)
            return redirect(ad_list)
        
    form = AdForm(instance = ads)
    return render(request,'myads.html',{'form':form})
def addelete(request,aid):
    ads = Ad.objects.get(id = aid)
    if request.method == 'POST':
        ads.delete()
        return redirect(ad_list)
    return render(request,'adel.html',{'ads':ads})

def sentmessage(request,aid):
    ads = Ad.objects.get(id = aid)
    reciever = ads.user
    form = ContactForm()
    if request.user.is_authenticated:
        if request.method=='POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                msg = form.save(commit=False)
                msg.sender = request.user
                msg.reciever = reciever
                msg.ad = ads
                msg.save()
                print(f"Message sent! Sender: {msg.sender}, Receiver: {msg.reciever}, Ad: {msg.ad}")
                return redirect(addetailpage,aid)
    

        
    return render(request,'sentmsg.html',{'form':form})

def inbox(request):
    if request.user.is_authenticated:
        msg = Contact.objects.filter(reciever=request.user)
        print(msg)
        return render(request,'inbox.html',{'msg':msg})
    else:
        return redirect(loginpage)
def search_ads(request):
    query = request.GET.get('q')
    # category = request.GET.get('category')
    ads = Ad.objects.all()
    
    
    if query:
        ads = ads.filter(models.Q(title__icontains = query)|models.Q(category__title__icontains=query))
        
  
   
    categories = Category.objects.all()
    return render(request,'searchresults.html',{'ads':ads,'categories':categories})  

def addetailpage(request,aid):
    ads = Ad.objects.get(id=aid)
    adi = Adimage.objects.filter(ad = ads)
    receiver = ads.user
    return render(request,'addetail.html',{'ads':ads,'adi':adi,'receiver':receiver})



def allcategory(request):
    print('view fuction called!')
    cat = Category.objects.all()
    print(cat)
    return render(request,'allcategory.html',{'cat':cat})

def categorylist(request,cid):
    ads = Ad.objects.filter(category = cid)
    return render(request,'searchresults.html',{'ads':ads})

def chat_page(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = ChatMessage.objects.filter(
        sender=request.user, receiver=receiver
    ) | ChatMessage.objects.filter(
        sender=receiver, receiver=request.user
    )
    
    return render(request, 'chat_page.html', {
        'receiver': receiver,
        'messages': messages
    })

@csrf_exempt
@login_required
def send_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        receiver = User.objects.get(id=data['receiver_id'])
        msg = ChatMessage.objects.create(
            sender=request.user,
            receiver=receiver,
            message=data['message']
        )
        return JsonResponse({
            'status': 'ok',
            'message': msg.message,
            'sender': request.user.username
        })
    
def allmessages(request):
    messages = ChatMessage.objects.filter(receiver = request.user).order_by('-timestamp')

    unique_messages = {}
    
    for message in messages:
        if message.sender not in unique_messages:
            unique_messages[message.sender] = message

        messages = list(unique_messages.values())
    return render(request,'allmessages.html',{'messages':messages})



