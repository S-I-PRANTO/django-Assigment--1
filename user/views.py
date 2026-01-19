from django.shortcuts import render,redirect,HttpResponse
from user.forms import CustomRegisterForm,Sign_In,AssignRoleForm,CreateGroupForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.decorators import user_passes_test
from task.models import Category,Event
from django.db.models import Count,Q

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_user(user):
    return user.groups.filter(name='user').exists()


@login_required
def dashboard_redirect(request):
    user = request.user

    if is_admin(user):
        return redirect('adminDashboard')

    elif is_organizer(user):
        return redirect('organize')

    elif is_user(user):
        return redirect('user')

    else:
        return redirect('no_permission')


@login_required
def UserDash(request):
    return render(request,'userNav.html')

@login_required
def AdminEventVeiw(request,id):
    view_task=Event.objects.select_related('category').prefetch_related('participants').get(id=id)
      
    return render(request, 'admin/AdminEvent.html',{
        'viewTask':view_task
        })



@login_required
@user_passes_test(is_admin ,login_url='no_permission')
def AdminEvent(request):
    query = request.GET.get('searchText', '') 
    base_query = Event.objects.select_related('category').annotate(participants_count=Count('participants'))

    if query:
        events = base_query.filter( Q(Event_Name__icontains=query) | Q(location__icontains=query)
        )
    else:
        events = base_query

    return render(request, 'admin/AdminEvent.html',{
        'events': events,
        'query': query,
    })



@login_required
@user_passes_test(is_admin ,login_url='no_permission')
def AdminCategory(request):
    categories = Category.objects.all()
    return render(request, 'admin/AdminCategory.html', {
        'categories': categories
    })



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
                return redirect('Dashboard')
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

@login_required
def admin_dashboard(request):
    return render(request,'Dashboard/dashboard.html')


@login_required
@user_passes_test(is_admin ,login_url='no_permission')
def admin_UserList(request):
    users=User.objects.prefetch_related(
        Prefetch('groups',queryset=Group.objects.all(),to_attr='all_groups'
                 )).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request,'admin/userList.html',{"users":users})

@login_required
@user_passes_test(is_admin ,login_url='no_permission')
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



@login_required
@user_passes_test(is_admin ,login_url='no_permission')
def create_group(request):
    form=CreateGroupForm()
    if request.method =='POST':
        form=CreateGroupForm(request.POST)
        if form.is_valid():
            group=form.save()
            messages.success(request,f"Group {group.name} has been created successfully ")
            return redirect('createGroup')

    return render(request,'admin/create_group.html',{'form':form})


@login_required
@user_passes_test(is_admin)
def group_list(request):
    groups=Group.objects.prefetch_related('permissions').all()
    return render(request,'admin/groupList.html',{'groups':groups})

def Participent(request):
    participants=User.objects.prefetch_related('Event')
    context={'participants':participants}
    return render(request,'admin/Participateshow.html',context)

@login_required
@user_passes_test(is_organizer)
def Organize(request):
    return render(request,'organizeNav.html')


@login_required
@user_passes_test(is_organizer)
def OrganizeEvent(request):
    query = request.GET.get('searchText', '') 
    base_query = Event.objects.select_related('category').annotate(participants_count=Count('participants'))

    if query:
        events = base_query.filter( Q(Event_Name__icontains=query) | Q(location__icontains=query)
        )
    else:
        events = base_query

    return render(request, 'Organize/OrganizeEvent.html',{
        'events': events,
        'query': query,
    })



@login_required
@user_passes_test(is_organizer)
def OrganizeCategory(request):
    categories = Category.objects.all()
    return render(request, 'Organize/OrganizeCategory.html', {
        'categories': categories
    })

@login_required
@user_passes_test(is_organizer)
def OrganizeEventVeiw(request,id):
    view_task=Event.objects.select_related('category').prefetch_related('participants').get(id=id)
      
    return render(request, 'Organize/OrganizeEvent.html',{
        'viewTask':view_task
        })