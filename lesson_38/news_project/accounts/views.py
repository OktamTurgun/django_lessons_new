from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views import View

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
