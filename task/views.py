
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
# from django.contrib.auth.models import User
from task.form import CategoryForm, EventForm
from task.models import Event,Category
from django.db.models import Count,Q
from datetime import date
from django.contrib.auth.decorators import user_passes_test,login_required,permission_required
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User=get_user_model()
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_user(user):
    return user.groups.filter(name='user').exists()

def admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)


def home(request):
    if request.user.is_authenticated:
        return redirect('Loginhome')
    else:
        return render(request, 'defaultHome.html')




@method_decorator(login_required,name='dispatch')
class Loginhome(TemplateView):

    def get_template_names(self):
        user = self.request.user
        if user.groups.filter(name='Admin').exists() or user.is_superuser:
           return ['admin/Admindashboard.html']
        elif user.groups.filter(name='Organizer').exists():
           return ['Organize/Organizedashboard.html']
        elif user.groups.filter(name='user').exists():
           return  ['userNav.html']
        return['defaultHome.html']

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        types=self.request.GET.get('type','all')
        todayDate=date.today()
        totalParticipate = User.objects.aggregate(participantTotal=Count('id'))
        totalEvents = Event.objects.aggregate(total_Task=Count('id'))
        upcomingEvents_count = Event.objects.filter(data__gt=todayDate).aggregate(Upcome_Task=Count('id'))
        past_Events_count = Event.objects.filter(data__lt=todayDate).aggregate(Past_Task=Count('id'))
        todaysEvent = Event.objects.filter(data=todayDate).select_related('category')
        baseFilter = Event.objects.select_related('category').prefetch_related('participants')
        if types == 'pariticipant':
            showtask=baseFilter

        elif types == 'upcome':
            showtask=baseFilter.filter(data__gt=todayDate)
        elif types == 'past':
            showtask=baseFilter.filter(data__lt=todayDate)
    
        else:showtask=baseFilter

        context['pariticipants']=totalParticipate
        context['event']=totalEvents
        context['upcome']=upcomingEvents_count
        context['past']=past_Events_count
        context['todayEvents']=todaysEvent
        context['showtask']=showtask
        context['types']=types

        return context


@method_decorator(login_required,name='dispatch')
class participant(ListView):
    model = User
    context_object_name = 'participants'
    template_name='Dashboard/pariticipant.html'
    def get_queryset(self):
        return User.objects.prefetch_related('RBAC')



@method_decorator(login_required,name='dispatch')
class category(ListView):
    model=Category
    template_name='Dashboard/category.html'
    context_object_name='categories'

    def get_queryset(self):
        return Category.objects.all()
    

@method_decorator(login_required,name='dispatch')
class event(ListView):
    model=Event
    template_name='Dashboard/event.html'
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
    

@method_decorator(login_required,name='dispatch')
class EventVeiw(DetailView):
    model=Event
    template_name='Dashboard/event.html'
    context_object_name='viewTask'
    pk_url_kwarg='id'
    def get_queryset(self):
        return Event.objects.select_related('category').prefetch_related('participants')

      

TaskCreateDecorated=[login_required,permission_required('task.add_task',login_url='no_permission')]
@method_decorator(TaskCreateDecorated,name='dispatch')    
class TaskCreate(CreateView):
    model=Event
    form_class=EventForm
    template_name='form.html'
    context_object_name='event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['category']= CategoryForm(self.request.POST)

        else :
            context['category']=CategoryForm()
            context["event"] = EventForm()

        return context
    

    def form_valid(self, form):
        context=self.get_context_data()
        category_form= context['category']

        if category_form.is_valid():
            category = category_form.save()
            event = form.save(commit=False)
            event.category = category
            event.save()
            form.save_m2m()
            messages.success(self.request, "Event Created Successfully")
            return redirect("form")

        return super().form_invalid(form)
        


    # category_form = CategoryForm()
    # event_form = EventForm()

    # if request.method == "POST":
    #     category_form = CategoryForm(request.POST)
    #     event_form = EventForm(request.POST,request.FILES)

    #     if category_form.is_valid() and event_form.is_valid():
    #         category = category_form.save()
    #         event = event_form.save(commit=False)
    #         event.category = category
    #         event.save()
    #         event_form.save_m2m()
    #         messages.success(request, "Event Created Successfully")
    #         return redirect("form")

    # context = {
    #     "category": category_form,
    #     "event": event_form,
    # }
    # return render(request, "form.html", context)



@user_passes_test(admin_or_organizer,login_url='no_permission')
@login_required
def Update(request, id):
    types = request.GET.get("type","Event")

    arr = []
    if types not in arr:
        if arr:
            arr.pop()
        arr.append(types)
    if types=='Event':
           objectType = get_object_or_404(Event, id=id)
           form_populated=EventForm
           
    elif types=='Category':
           objectType = get_object_or_404(Category, id=id)
           form_populated=CategoryForm
           

    if request.method == "POST":
            form = form_populated(request.POST, instance=objectType)
            if form.is_valid():
                form.save()
                messages.success(request,F"{types} updated successfully")
                return redirect("update", id=id)
    
    else:
        form = form_populated(instance=objectType)


    context = {
        "form": form,
        'arr':arr
    }
    return render(request, "Dashboard/update.html", context)


@user_passes_test(admin_or_organizer,login_url='no_permission')
@login_required
def Delete_event(request, id):
    types = request.GET.get("type", "event")
    print(types)
   
    if types == 'event':
        objectType = Event.objects.get(id=id)
        urls = 'event' 

    elif types == 'category':
        objectType = Category.objects.get(id=id)
        urls = 'category'  


    if request.method == "POST":
        objectType.delete()
        messages.success(request, f"{types} Deleted successfully")
        return redirect(urls)  

    else:
        messages.error(request, f"Something went wrong")
         
    

    return redirect(urls)



def Rsvp(request,id):
    if request.method=='POST':
        event=get_object_or_404(Event,id=id)
        user = request.user
        if event.participants.filter(id=user.id).exists():
            messages.warning(request, "You have already RSVP for this event")
        else:
            event.participants.add(user)
            messages.success(request, "RSVP successful. Please check your confirmation email.")

    return redirect('show_rsvp')

def showRsvp(request):

    if request.user.is_superuser:
        rsvp_events = request.user.RBAC.all()
        template = 'admin/AdminRsvp.html'
    else:
        rsvp_events = request.user.RBAC.all()
        template = 'Dashboard/userDashboard.html'
        

    context={'events':rsvp_events}

    return render(request, template, context)