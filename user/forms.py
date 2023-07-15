from .models import cliente
from django import forms
from django.forms import ModelForm
from user.models import User ,contrato ,valores, retiro, interes
from django.contrib.auth.forms import UserCreationForm


class ContratoForm(forms.ModelForm):
    class Meta:
        model = contrato
        fields = ['id','NomCliente','inversion','fechaIncio','fechaFin','usuarioC']
        widgets = {
            'fechaIncio': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
            'fechaFin': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
}

class NuevoContratoForm(forms.ModelForm):
    class Meta:
        model = contrato
        fields = ['id','NomCliente','inversion','fechaIncio','fechaFin','usuarioC']
        widgets = {
            'fechaIncio': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
            'fechaFin': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
}
        
class ValoresForm(forms.ModelForm):
    class Meta:
        model = valores
        fields = ['id','contrato','interesDia','fechaDia','SubTotal']
        widgets = {
            'fechaDia': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
            
        }

class RetiroForm(forms.ModelForm):
    class Meta:
        model = retiro
        fields = ['id','contrato','fechaRetiro','valorRetiro']
        widgets = {
            'fechaRetiro': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['id','username']

class clienteForm(ModelForm):
    class Meta:
        model = cliente
        fields = ['usuario','nombre','apellido','correo','telefono','estado']

class loginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

    
class InteresForm(forms.ModelForm):
    class Meta:
        model = interes
        fields = ['id','contrato','sumainteres','fechainicio','fechafin']
        widgets = {
            'fechainicio': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
            'fechafin': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }),
}