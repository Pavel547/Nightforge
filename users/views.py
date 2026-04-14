from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from .models import CustomUser
from cart.views import CartMixin

# User registration view with merge carts after auto login
def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:index')
    
    if request.method == 'POST':
        next_url = request.POST.get('next') or request.GET.get('next')
        old_session = request.session.session_key
        
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            cart_mixin = CartMixin()
            cart_mixin.merge_carts(request, old_session)
            
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                return redirect(next_url)
            else:
                return redirect('main:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

#Login view with merging old and new carts 
def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:index')
    
    if request.method == 'POST':
        next_url = request.POST.get('next') or request.GET.get('next')
        old_session = request.session.session_key
        
        form = CustomUserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            cart_mixin = CartMixin()
            cart_mixin.merge_carts(request, old_session)   

            if next_url and url_has_allowed_host_and_scheme(next_url, 
                allowed_hosts={request.get_host()}, 
                require_https=request.is_secure()
                ):
                return redirect(next_url)
            else:
                return redirect('main:index')
    else:
        form = CustomUserLoginForm()

    return render(request, 'users/login.html', {'form': form})

@login_required(login_url='/users/login')
def profile_view(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'users/profile.html', {'user': user})

@login_required(login_url='/users/login')
def edit_account_details(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            
            if next_url and url_has_allowed_host_and_scheme(next_url,
                allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_url)
            else:
                return redirect('users:profile')
                
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'users/edit_account_details.html', {'form': form})

@login_required(login_url='/users/login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main:index')
    return render(request, 'users/logout_confirm.html')
    
class API_Register(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.data, status.HTTP_400_BAD_REQUEST)
        