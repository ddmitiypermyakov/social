from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import Person, City


class UserRegisterForm(forms.ModelForm):
    # username = forms.CharField(required=True, label='Имя пользователя')
    username= forms.CharField(required=True, label='Имя пользователя',widget=forms.TextInput(
    attrs={'class': 'form-control'}),
    help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.')
    # content_user = forms.CharField(required=True, label='Контент пользователя')
    email = forms.EmailField(required=True, label='Адрес электронной почты ', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text='Введите тот же самый пароль еще раз для проверки')
    first_name= forms.CharField(required=True, label='Имя',widget=forms.TextInput(
    attrs={'class': 'form-control'}))
    last_name= forms.CharField(required=True, label='Имя',widget=forms.TextInput(
    attrs={'class': 'form-control'}))

    phone = forms.IntegerField (label='Телефон', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(queryset=City.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}))
    # photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        # print('Из клинметоад',self.photo)
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_actived = True
        if commit:
            user.save()

        # user_registered.send(UserRegisterForm, instance=user)
        return user

    class Meta:
        model = Person
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'send_messages',
                  'phone', 'city', 'birthday', 'photo',
                  'gender')


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label= 'Адрес электронной почты')

    class Meta:
        model = Person
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages', 'phone', )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SearchForm(forms.Form):
    keyword= forms.CharField(required=False,max_length=20, label='')


# class UserRegisterForm(UserCreationForm):
#     username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label='Подтверждение пароля',
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

class Person1Form(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ('phone',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = Person.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['city'].queryset = Person.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass  # неверный ввод от клиента; игнорирование и возврат к пустому набору запросов City
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.region.city_set.order_by('name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['district'].queryset = District.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.city.district_set.order_by('name')