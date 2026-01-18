
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from task.form import CategoryForm, EventForm
from task.models import Event,Category
from django.db.models import Count,Q
from datetime import date
from django.contrib.auth.decorators import user_passes_test,login_required

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_user(user):
    return user.groups.filter(name='user').exists()

def admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)
def home(request):
    return render(request,'defaultHome.html')



@login_required
def Loginhome(request):
    types=request.GET.get('type','all')
    todayDate=date.today()

    total_participants = User.objects.aggregate(Total_participant=Count('id'))
    total_events = Event.objects.aggregate(total_Task=Count('id'))
    upcoming_events_count = Event.objects.filter(data__gt=todayDate).aggregate(Upcome_Task=Count('id'))
    past_events_count = Event.objects.filter(data__lt=todayDate).aggregate(Past_Task=Count('id'))
    todaysEvent = Event.objects.filter(data=todayDate).select_related('category')
    rsvp_events = request.user.RBAC.all()
    baseFilter = Event.objects.select_related('category').prefetch_related('participants')
    if types == 'pariticipant':
        showtask=baseFilter

    elif types == 'upcome':
        showtask=baseFilter.filter(data__gt=todayDate)
    elif types == 'past':
        showtask=baseFilter.filter(data__lt=todayDate)
   
    else:showtask=baseFilter

    

    context={   'pariticipants':total_participants,
                'event'        :total_events,
                'upcome'       :upcoming_events_count,
                'past'         :past_events_count,
                'todayEvents'  :todaysEvent,
                'showtask'     :showtask,
                'types'        :types,
                'rsvp'          :rsvp_events
             }
    
    user = request.user
    if user.groups.filter(name='Admin').exists() or user.is_superuser:
        template_name = 'admin/Admindashboard.html'
    elif user.groups.filter(name='Organizer').exists():
        template_name = 'Organize/Organizedashboard.html'
    elif user.groups.filter(name='user').exists():
        template_name = 'userNav.html'
    else: template_name='defaultHome.html'
    return render(request,template_name,context)



@login_required
def participant(request):
    participants=User.objects.prefetch_related('RBAC')
    context={'participants':participants}
    return render(request,'Dashboard/pariticipant.html',context)


@login_required
def category(request):
    categories = Category.objects.all()
    return render(request, 'Dashboard/category.html', {
        'categories': categories
    })

@login_required
def event(request):
    # event = Event.objects.prefetch_related('participant').select_related('category').get(id=id)
    query = request.GET.get('searchText', '') 
    base_query = Event.objects.select_related('category').annotate(participants_count=Count('participants'))

    if query:
        events = base_query.filter( Q(Event_Name__icontains=query) | Q(location__icontains=query)
        )
    else:
        events = base_query

    return render(request, 'Dashboard/event.html',{
        'events': events,
        'query': query,
    })

@login_required
def EventVeiw(request,id):
    view_task=Event.objects.select_related('category').prefetch_related('participants').get(id=id)
      
    return render(request, 'Dashboard/event.html',{
        'viewTask':view_task
          })
@login_required
@user_passes_test(admin_or_organizer)
def form(request):
    category_form = CategoryForm()
    event_form = EventForm()

    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        event_form = EventForm(request.POST,request.FILES)

        if category_form.is_valid() and event_form.is_valid():
            category = category_form.save()
            event = event_form.save(commit=False)
            event.category = category
            event.save()
            event_form.save_m2m()
            messages.success(request, "Event Created Successfully")
            return redirect("form")

    context = {
        "category": category_form,
        "event": event_form,
    }
    return render(request, "form.html", context)


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
        user=get_object_or_404(Event,id=id)
        if user.participants.filter(id=request.user.id).exists():
          messages.warning(request, "You have already RSVP for this event")
        else:
            user.participants.add(request.user)
            messages.success(request, "RSVP successful Pleace Check Your Confirmation email.")

    return redirect('show_rsvp')

def showRsvp(request):
    rsvp_events = request.user.RBAC.all()
    return render(request, 'Dashboard/userDashboard.html', {'events': rsvp_events})