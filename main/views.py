from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
from  django.contrib.auth.forms import UserCreationForm
from .forms import *
# Create your views here.

def by_person(request,pk):
    person = get_object_or_404(Person, pk=pk)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q=Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword)
        person = person.filter(q)
    else:
        keyword=''
    form = SearchForm(initial={'keyword' : keyword})
    paginator = Paginator(person,2)
    if 'page' == request.GET:
        page_num=request.GET['page']
    else:
        page_num=1
    page=paginator.get_page(page_num)
    context= {'person':page.object_list, 'page': page, 'form' : form}
    return render(request, 'main/by_person.html',context)

class UserRegisterView(CreateView):
    model = Person
    template_name = 'main/register/register_user.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('register_done')

class UserRegisterDoneView(TemplateView):
    template_name = 'main/register/register_done.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Person
    template_name = 'main/change/change_profile.html'
    form_class = ChangeUserInfoForm
    success_url= reverse_lazy('home')
    success_message='Данные пользователя изменены'

    def setup(self,request,*arg,**kwargs):
        self.user_id = request.user.pk
        return super().setup(request,*arg,**kwargs)

    def ger_object(self, queryset=None):
        if not queryset:
            queryset= self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
# def register(request):
#
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы учспешно зарегистрировались')
#             return redirect('home')
#         else:
#             messages.error(request, 'Ошибка регистрации')
#     else:
#         form = UserRegisterForm()
#     context = {'form': form}
#     return render(request,'main/register.html',context)




def user_login(request):
    if request.method == 'POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():

            user=form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form= UserLoginForm()
    context = {'form': form}
    return render(request,'main/login.html',context)

def user_logout(request):
    logout(request)
    return redirect('home')


def mane_page(request):
    persons = Person.objects.all()
    genders = Gender.objects.all()
    context = {'persons': persons, 'title': 'Главная страница','genders': genders}
    return render(request, 'main/mane_page.html', context)


def get_gender(request,gender_id):
    persons = Person.objects.filter(gender_id=gender_id)
    genders = Gender.objects.all()
    gender = Gender.objects.get(pk=gender_id)
    context = {'persons': persons, 'genders': genders, 'gender' : gender}
    return render(request, 'main/gender.html', context)

def get_profile(request,pk):
    persons = Person.objects.filter(pk=pk)

    context = {'persons': persons}
    return render(request, 'main/profile.html', context)

def sort_profile(request):

    persons = Person.objects.order_by("-city")

    context = {'persons': persons}
    return render(request, 'main/sort_profile.html', context)

def sort_profile_bith(request):
    persons = Person.objects.order_by("-birthday")

    context = {'persons': persons}
    return render(request, 'main/sortbith.html', context)

# class Search(ListView):
#     template_name = 'main/search.html'
#     context_object_name='posts'
#
#     def get_queryset(self):
#         return Person.objects.filter(first_name__icontains = self.request.GET.get('s'))
#


