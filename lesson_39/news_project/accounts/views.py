from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views import View
from .models import Profile

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
        return redirect('news:home')
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

# variant 1 signup view uchun function bilan
# def signup_view(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()  # user saqlanadi
#             return render(request, "accounts/register_done.html")  
#     else:
#         form = UserRegistrationForm()
#     return render(request, "accounts/register.html", {"form": form})

# variant 2 signup view CreateView bilan
class SignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:register_done')

    def form_valid(self, form):
      # form.save() parolni ham hashlaydi, chunki biz save() metodini override qilganmiz
      form.save()
      return super().form_valid(form) 
    
# variant 3 signup view uchun View bilan
# class SignupView(View):
#     def get(self, request):
#         form = UserRegistrationForm()
#         return render(request, "accounts/register.html", {"form": form})
    
#     def post(self, request):
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()  # user saqlanadi
#             return render(request, "accounts/register_done.html")  
#         return render(request, "accounts/register.html", {"form": form})

def edit_profile(request):
    user = request.user

    # Agar profil bo'lmasa, yaratib qo'yamiz
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    if request.method == 'POST':
        user_form = UserEditForm(instance=user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:user_profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=user.profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })