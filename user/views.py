from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from user.forms import CustomRegisterForm,Sign_In,AssignRoleForm,CreateGroupForm,EditProfileForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from task.models import Category,Event
from django.db.models import Count,Q
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,FormView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from user.forms import CustomPasswordChange,CustomPasswordResetView,CustomPasswordResetConfirm
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.contrib.auth import get_user_model
User=get_user_model()
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


@method_decorator(login_required,name='dispatch')
class UserDash(TemplateView):
   template_name='userNav.html'

# @login_required
# def AdminEventVeiw(request,id):
#     view_task=Event.objects.select_related('category').prefetch_related('participants').get(id=id)
#     return render(request, '',{
#         'viewTask':view_task
#         })

@method_decorator(login_required,name='dispatch')
class AdminEventVeiw(DetailView):
    model=Event
    template_name='admin/AdminEvent.html'
    context_object_name='viewTask'
    pk_url_kwarg='id'
    def get_queryset(self):
        return Event.objects.select_related('category').prefetch_related('participants')

      

class ChangePasswords(PasswordChangeView):
    template_name='accounts/changePassword.html'
    form_class=CustomPasswordChange

class CustomPasswordReset(PasswordResetView):
    form_class=CustomPasswordResetView
    template_name='accounts/password_reset_form.html'   
    success_url=reverse_lazy('sign_in')
    html_email_template_name='accounts/CustomEmailReset.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portocol']='https'if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        
        return context

    def form_valid(self, form):
        messages.success(self.request,'A Reset email sent. Please check your email')
        return super().form_valid(form)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirm
    template_name='accounts/password_reset_form.html'   
    success_url=reverse_lazy('sign_in')
    
    def form_valid(self, form):
        messages.success(self.request,'Password has been reset successfully')
        return super().form_valid(form)
    


AdminEventDecoretor=[login_required,user_passes_test(is_admin ,login_url='no_permission')]
@method_decorator(AdminEventDecoretor,name='dispatch')
class AdminEvents(ListView):
    model=Event
    template_name='admin/AdminEvent.html'
    context_object_name='events'

    def get_queryset(self):
        query = self.request.GET.get('searchText', '') 
        base_query = Event.objects.select_related('category').annotate(participants_count=Count('participants'))

        if query:
            events = base_query.filter( Q(Event_Name__icontains=query) | Q(location__icontains=query)
            )
        else:
            events = base_query

        return events
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] =self.request.GET.get('searchText', '') 
        return context
    

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
        return redirect('Dashboards')
    
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



AssignRoleDecoretor=[login_required,user_passes_test(is_admin ,login_url='no_permission')]
@method_decorator(AssignRoleDecoretor,name='dispatch')
class assign_role(FormView):
    template_name = 'admin/assing_role.html'
    form_class = AssignRoleForm

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        role = form.cleaned_data.get('role')
        self.user.groups.clear()
        self.user.groups.add(role)
        messages.success(
            self.request,
            f"User {self.user.username} has been assigned to the {role.name} role"
        )
        return redirect('adminUserlist')
    




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

class CustomProfileView(TemplateView):
    template_name='accounts/Profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user

        if user.is_superuser:
            base = 'adminNav.html'
        elif user.groups.filter(name='Organizer').exists():
            base = 'organizeNav.html'
        else:
            base = 'userNav.html'

        context['base_template'] = base
        context['username']=user.username
        context['email']=user.email
        context['name']=user.get_full_name
        context['profile_image']=user.profile_image
        context['phone_number']=user.phone_number
        context['bio']=user.bio
        context['member_Since']=user.date_joined
        context['last_login']=user.last_login
        return context
    

class EditProfileView(UpdateView):
    model=User
    form_class=EditProfileForm
    template_name='accounts/Update_profile.html'
    context_object_name='form'
  

    def get_object(self):
        return self.request.user

    
    def form_valid(self, form):
        form.save()
        return redirect('profile')