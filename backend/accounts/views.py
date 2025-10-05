from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import OrgUserLoginForm, OrgUserSignupForm, Organization

def signup_view(request):
    if request.method == 'POST':
        form = OrgUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shop_home')
    else:
        form = OrgUserSignupForm()
    
    organizations = Organization.objects.all()
    
    return render(request, 'signup.html', {
        'form': form,
        'organizations': organizations
    })

def login_view(request):
    if request.method == 'POST':
        form = OrgUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop_home')
    else:
        form = OrgUserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('shop_home')
