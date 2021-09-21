from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from account.forms import RegistrationForm,LoginForm
# Create your views here.
def registeration_view(request):
    context={}
    if request.POST:
        form=RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            print("ppp")
            form.save()
            return redirect("default")
        else:
            context['registration_form']=form
    else:
        form = RegistrationForm()
        context['registration_form']=form
    return render(request,'account/sign_up.html',context)


def default_view(request):
    return render(request,'account/default.html')


def signout_view(request):
    logout(request)
    return render(request,'account/sign_out.html')


def signin_view(request):
    context={}

    user=request.user
    if user.is_authenticated:
        print('ppp')
        return redirect('home')

    if request.POST:
        form=LoginForm(request.POST)
        if form.is_valid:
            email=request.POST['email']
            password=request.POST['password']

            user=authenticate(email=email,password=password)


            if user:
                login(request,user)
                return redirect('home')


    else:
        form=LoginForm()
        print(form)
    context['login_form']=form

    return render(request,'account/sign_in.html',context)

def home_view(request):

    return render(request,'stocks/home.html')
