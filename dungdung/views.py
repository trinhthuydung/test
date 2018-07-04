from django.shortcuts import render,HttpResponse,redirect
from dungdung import models
from django.contrib.sites.shortcuts import  get_current_site
from django.utils.encoding import force_bytes,force_text
from dungdung.token import adljj
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.db.models import Q

# đay la thu vien Query su dung nhieu trong cau lenh truy van

# Create your views here.
def registration(request):
    data=  {}
    error = {}
    if request.method == 'POST':
        data['email'] = request.POST.get('Email')
        data['name'] = request.POST.get('Name')
        data['password'] = request.POST.get('Password')
        count1 = models.AuthUser.objects.filter(email=data['email']).count()
        if count1 > 0:
            error['exist1'] = 'This email already exist!'
        else:
            b = models.AuthUser(username=data['name'], email = data['email'],password=data['password'])
            b.save()
            # b = models.AuthUser.objects.get(username= 'dunghihi')
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account'
            message = render_to_string('active_email.html',{
                'user': b,
                'domain' : current_site.domain,
                'uid' : urlsafe_base64_encode(force_bytes(b.pk)).decode(),
                'token': adljj.make_token(b),
            })
            to_email = data['email']
            # to_email = 'dung.ttt140704@sis.hust.edu.vn'
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return  HttpResponse('Please confim hihi')

    return render(request,'registration.html',{'data':data,'error':error})
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = models.AuthUser.objects.get(pk= uid)
    except(TypeError,ValueError, OverflowError, models.AuthUser.DoesNotExist):
        user = None
    if user is not None and adljj.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse("Thank you Dung !")
    else:
        return HttpResponse("Sorry Dung!")

def login1(request):
    error ={}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        AuthUser = models.AuthUser.objects.filter(Q(username=username)|Q(email=username),Q(is_active=1),Q(password=password))
        count = AuthUser.count()
        if(count > 0):
            login(request, AuthUser[0])
            request.session['username'] = AuthUser[0].username
            request.session.set_expiry(0)
            return redirect('home')
        else:
            error['exist'] = "This email or username is false"

    return render(request, 'login.html', {'error': error})
def home(request):
    data = {}
    if request.session.has_key('username'):
        AuthUser = models.AuthUser.objects.get(username=request.session['username'])
        data['hello'] = "Hello " + AuthUser.username + "!"
        return render(request, 'home.html', {'data':data})
    else:
        return redirect('login')


def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return HttpResponse("Good bye!")

def input(request):
    a = models.AuthUser.objects.all()
    print(a)
    if '_delete' in request.POST:
        for data in a:
            if request.POST.get('%d' %data.id):
                data.delete()
        return redirect('input')
    elif '_edit' in request.POST:
        for data in a:
            if request.POST.get('%d' % data.id):
                if request.POST.get('username') != "":
                    data.username = request.POST.get('username')
                if request.POST.get('email') != "":
                    data.email = request.POST.get('email')
                if request.POST.get('password') != "":
                    data.password = request.POST.get('password')
        return redirect('input')
    return render(request, 'input.html', {'a':a})

def myform(request):
    data={}
    if request.method =="POST":
        data['name'] = request.POST.get('name')
        data['address'] = request.POST.get('address')
        data['phone'] = request.POST.get('phone')
        data['job'] = request.POST.get('job')
        a = models.form(name=data['name'], address=data['address'], phone=data['phone'], job=data['job'])
        a.save()
    return render(request, 'My form.html', {'data':data} )
def load(request):
    b = models.form.objects.all()
    print(b)
    return render(request, 'My form.html', {'load':b})




