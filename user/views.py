from django.shortcuts import render,redirect,HttpResponse
from user.forms import CustomRegisterForm,Sign_In,AssignRoleForm,CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def UserDash(request):
    return render(request,'common.html')
def Sign_up(request):
    form = CustomRegisterForm()
    if request.method == 'POST':
        form=CustomRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active=False
            user.save()
            messages.success(request,"Send the mail. Please check your email")
            return redirect('sign_in')

    return render(request,'Auth/Registation.html',{'form':form})


def Sign_in(request):
    form=Sign_In()
    if request.method == 'POST':
        form=Sign_In(data=request.POST)
        if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('home')
    return render(request,'Auth/login.html',{'form':form})
@login_required
def Sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign_in')
    
def activate_user(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            return redirect('sign_in')
        else:
            return HttpResponse("Invail Id & token")
    
    except User.DoesNotExist:
        return HttpResponse("User not Found")
    
@user_passes_test(is_admin,login_url='no-permission')
def admin_dashboard(request):
    users=User.objects.prefetch_related(
        Prefetch('groups',queryset=Group.objects.all(),to_attr='all_groups'
                 )).all()
    for user in users:
        if user.all_groups:
            user.groups_name=user.all_groups[0].name
            user.groups_name='No Group Assigned'
    return render(request,'admin/dashboard.html',{"users":users})

@user_passes_test(is_admin,login_url='no-permission')
def assign_role(request,user_id):
    user=User.objects.get(id=user_id)
    form=AssignRoleForm()
    if request.method=="POST":
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f"User {user.username} has been assigned to the {role.name} role")
            return redirect('adminDashboard')
    
    return render(request,'admin/assing_role.html',{'form':form})
@user_passes_test(is_admin,login_url='no-permission')
def create_group(request):
    form=CreateGroupForm()
    if request.method =='POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f"Group {group.name} has been created successfully ")
            return redirect('createGroup')

    return render(request,'admin/create_group.html',{'form':form})
@user_passes_test(is_admin,login_url='no-permission')
def group_list(request):
    groups=Group.objects.prefetch_related('permissions').all()
    return render(request,'admin/groupList.html',{'groups':groups})
