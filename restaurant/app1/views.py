


from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView,ListView
from app1.models import MenuItem,Menu


# Create your views here.

def home(request):
    m=Menu.objects.all()
    context={'menu':m}
    return render(request,'home.html',context)
class Add(CreateView):
    model = MenuItem
    template_name = 'add.html'
    fields = ['name','price','menu','is_vegetarian']
    success_url = reverse_lazy('home')

class Itemview(DetailView):
    model = Menu
    template_name = 'view.html'
    context_object_name = 'm'

class Update(UpdateView):
    model = MenuItem
    template_name = 'update.html'
    fields = ['price']
    success_url = reverse_lazy('home')

class Menulist(ListView):
    model=Menu
    template_name='list.html'
    context_object_name='m'