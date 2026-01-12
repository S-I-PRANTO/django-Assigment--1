import re
from django import forms
from django.contrib.auth.models import User,Permission,Group
from django_password_eye.fields import PasswordEye
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

class maxinStyle:
    default_Style=' w-3/6 border border-gray-300 rounded px-3 py-2 m-3'

    def apply_style(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_Style ,
                    'placeholder':f"Enter {field.label.lower()}"
                })

            elif isinstance(field.widget,forms.EmailInput):
                    field.widget.attrs.update({
                    'class':self.default_Style,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.PasswordInput):
                    field.widget.attrs.update({
                    'class':self.default_Style,
                    'placeholder':f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                    field.widget.attrs.update({
                    'placeholder':f"Enter {field.label.lower()}"
                })

            else:
                field.widget.attrs.update({
                })

    
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_style()             

                


class CustomRegisterForm(maxinStyle,forms.ModelForm):
    password1 = PasswordEye(label="Password")
    confirm_password = PasswordEye(label="Confirm Password")
    class Meta:
        model= User
        fields=['first_name','last_name','username','email']


    def clean_email(self):
        email=self.cleaned_data.get('email')
        email_exists=User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email

    def clean(self):
        cleaned_data=super().clean()
        p1=cleaned_data.get('password1')
        p2=cleaned_data.get('confirm_password')

        if p1 :
            if len(p1) < 8:
                self.add_error('password1', "Minimum 8 characters required")
            if not re.search(r'[A-Z]', p1):
                self.add_error('password1', "Must contain an uppercase letter")
            if not re.search(r'[a-z]', p1):
                self.add_error('password1', "Must contain a lowercase letter")
            if not re.search(r'\d', p1):
                self.add_error('password1', "Must contain a number")
        
        if p1 and p2 and p1!=p2:
             self.add_error('confirm_password',"Passwords do not match")

        
        return cleaned_data
    
    # def passwordHash(self,commit=True):
    #      user=super().save(commit=False)
    #      user.set_password(self.cleaned_data['password1'])
    #      if commit:
    #         user.save()
    #      return user   
              



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None 
        self.apply_style()

class Sign_In(AuthenticationForm,maxinStyle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_style()


class AssignRoleForm(maxinStyle, forms.Form):
    role=forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role",
        widget=forms.Select(
        attrs={
        'class': 'form-select w-1/2 m-3 p-2 border rounded'
        }
        )
    )
class CreateGroupForm(maxinStyle, forms.ModelForm):

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

