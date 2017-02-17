from django import forms
from .models import MainSettings
from datetime import timedelta, datetime, tzinfo
from django.forms import ModelForm
 
class CheckBoxForm(forms.Form):
    #checkbox = forms.CharField(label='Your name', max_length=100)
    checkbox = forms.BooleanField
    
class MainSettingsForm(forms.ModelForm):

    user_login = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин', 'required': 'true'}))
    user_password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Пароль'}), required = True)
    user_password_confirm = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Подтверждение пароля'}), required = True)
    period = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'секунды'}))
    

    class Meta:
        model = MainSettings
        fields = '__all__'
        #fields = ['id_MainSettings', 'user_login', 'user_password', 'sync_time', 'sync_server', 'datetime', 'period', 'remote_server']
        
  
    # Валидация проходит в этом методе
    def clean(self):
        # Определяем правило валидации
        if self.cleaned_data.get('user_password') != self.cleaned_data.get('user_password_confirm'):
            # Выбрасываем ошибку, если пароли не совпали
            raise forms.ValidationError({'user_password_confirm':'Пароли должны совпадать!'})
        return self.cleaned_data
        
    