from typing import Any
from django import forms
from django.contrib.auth.models import User

class registroForm(forms.Form):
    username = forms.CharField(label='Identificacion', required=True, max_length=50, widget=forms.NumberInput(attrs={'id':'username','placeholder':'Numero de documento'}))
    nombre = forms.CharField(label='Nombre', required=True, max_length=50, widget=forms.TextInput(attrs={'id':'nombre','placeholder':'Nombres'}))
    apellido = forms.CharField(label='Apellido', required=True, max_length=50, widget=forms.TextInput(attrs={'id':'apellido','placeholder':'Apellido'}))    
    email = forms.CharField(label='Correo', required=True, max_length=50, widget=forms.EmailInput(attrs={'id':'email','placeholder':'@example.com'}))
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'id':'password','placeholder':'Ingrese contraseña'}))
    password2 = forms.CharField(label='Confirme contraseña', required=True, widget=forms.PasswordInput(attrs={'placeholder':'Corfirme contraseña'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya se encuentra en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Las contraseñas no coinciden')

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        nombre = self.cleaned_data.get('nombre')
        apellido = self.cleaned_data.get('apellido')

   
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = nombre
        user.last_name = apellido
        user.save()

        return user
    

class EditarPerfilForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('El usuario ya se encuentra en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user