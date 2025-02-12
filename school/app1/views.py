from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView,ListView,DetailView,View
from app1.models import School,Student
from django.contrib.auth.models import User
from app1.forms import Regform

from app1.forms import Schoolform

from django.contrib.auth import logout


# Create your views here.

class Home(TemplateView):
    template_name = 'home.html'


class Addschool(CreateView):
    template_name = 'addschool.html'
    form_class = Schoolform
    # fields = ['name','principal','location']
    model=School
    success_url = reverse_lazy('home')

class Addstudent(CreateView):
    template_name = 'addstudent.html'
    fields=['name','age','school']
    model=Student
    success_url = reverse_lazy('home')

class Schoollist(ListView):
    template_name='schoollist.html'
    model=School
    context_object_name='school'

    # def get_queryset(self):
    #     q=super().get_queryset()
    #     qs=q.filter(location='Kozhuvanal')
    #     return qs


    # def get_queryset(self):
    #     q=super().get_queryset()
    #     queryset=q.filter(name__startswith='G')
    #     return queryset

class Details(DetailView):
    template_name = 'details.html'
    model = School
    context_object_name = 'school'


class Details1(ListView):
    template_name = 'details1.html'
    model = Student
    context_object_name = 'student'

    # def get_queryset(self):
    #     q=super().get_queryset()
    #     queryset=q.filter(school__location='Kozhuvanal')
    #     return queryset


    # def get_queryset(self):
    #     q=super().get_queryset()
    #     queryset=q.filter(name__startswith='T')
    #     return queryset

    # def get_queryset(self):
    #     q=super().get_queryset()
    #     queryset=q.filter(age__gt=20)
    #     return queryset

    # def get_queryset(self):
    #     q=super().get_queryset()
    #     qs=q.filter(age__lt=20)
    #     return qs

    # def get_context_data(self):
    #     context=super().get_context_data()
    #     context['name']='Arun'
    #     context['school']=School.objects.all()
    #     return context

class Register(CreateView):
    model = User
    # fields = ['username','password','email','first_name','last_name']
    form_class = Regform
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):  # When password is not converted into
        u=form.cleaned_data['username']
        p = form.cleaned_data['password']
        e = form.cleaned_data['email']
        f = form.cleaned_data['first_name']
        l = form.cleaned_data['last_name']

        b=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
        b.save()
        return redirect('home')

class Login(LoginView):
    template_name = 'login.html'

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('login')