from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.
def user_login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      print(data)
      user = authenticate(
        request,
        username=data['username'],
        password=data['password']
      )
      if user is not None:
        login(request, user)
        return redirect('home')
      else:
        return render(request, 'accounts/login.html', {
          'form': form,
          'error': "Username yoki parol noto'g'ri!"
        })
  else:
    form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})
  

def dashboard_view(request):
  user = request.user

  context = {
    'user': user
  }

  return render(request, 'pages/user_profile.html', context)
