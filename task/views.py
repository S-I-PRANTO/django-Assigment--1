
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from task.form import CategoryForm, EventForm,ParticipantForm
from task.models import Event,Participant,Category
from django.db.models import Count,Q
from datetime import date
def home(request):
    types=request.GET.get('type','all')
    todayDate=date.today()

    total_participants = Participant.objects.aggregate(Total_participant=Count('id'))
    total_events = Event.objects.aggregate(total_Task=Count('id'))
    upcoming_events_count = Event.objects.filter(data__gt=todayDate).aggregate(Upcome_Task=Count('id'))
    past_events_count = Event.objects.filter(data__lt=todayDate).aggregate(Past_Task=Count('id'))
    todaysEvent = Event.objects.filter(data=todayDate).select_related('category')

    baseFilter = Event.objects.select_related('category').prefetch_related('participant')

    
    if types == 'event':
        showtask=baseFilter

    elif types == 'upcome':
        showtask=baseFilter.filter(data__gt=todayDate)
    elif types == 'past':
        showtask=baseFilter.filter(data__lt=todayDate)
    elif types == 'pariticipant':
        showtask=baseFilter
    else:showtask=baseFilter

    

    context={'pariticipants':total_participants,
             'event'        :total_events,
             'upcome'       :upcoming_events_count,
             'past'         :past_events_count,
             'todayEvents'  :todaysEvent,
             'showtask'         :showtask

             }
    return render(request,'Dashboard/dashboard.html',context)

def participant(request):
    participants=Participant.objects.prefetch_related('Event')
    context={'participants':participants}
    return render(request,'Dashboard/pariticipant.html',context)


def category(request):
    categories = Category.objects.all()
    return render(request, 'Dashboard/category.html', {
        'categories': categories
    })

def event(request):
#  event = Event.objects.prefetch_related('participant').select_related('category').get(id=id)
    query = request.GET.get('searchText', '') 
    base_query = Event.objects.select_related('category').annotate(participants_count=Count('participant'))

    if query:
        events = base_query.filter( Q(Event_Name__icontains=query) | Q(location__icontains=query)
        )
    else:
        events = base_query

    return render(request, 'Dashboard/event.html',{
        'events': events,
        'query': query,
    })
def EventVeiw(request,id):
    view_task=Event.objects.select_related('category').prefetch_related('participant').get(id=id)
      
    return render(request, 'Dashboard/event.html',{
        'viewTask':view_task
          })

def form(request):
    category_form = CategoryForm()
    event_form = EventForm()
    participant_form = ParticipantForm()

    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        event_form = EventForm(request.POST)
        participant_form = ParticipantForm(request.POST)

        if category_form.is_valid() and event_form.is_valid():
            category = category_form.save()
            event = event_form.save(commit=False)
            event.category = category
            event.save()

            if participant_form.is_valid():
                participant = participant_form.save()
                participant.Event.add(event)

            messages.success(request, "Event Created Successfully")
            return redirect("form")

    context = {
        "category": category_form,
        "event": event_form,
        "participant": participant_form,
    }
    return render(request, "form.html", context)

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
           
    elif types=='Participant':
           objectType = get_object_or_404(Participant, id=id)
           form_populated=ParticipantForm
           


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


def Delete_event(request, id):
    types = request.GET.get("type", "event")
    print(types)
   
    if types == 'event':
        objectType = Event.objects.get(id=id)
        urls = 'event' 

    elif types == 'category':
        objectType = Category.objects.get(id=id)
        urls = 'category'  

    elif types == 'participant':
        objectType = Participant.objects.get(id=id)
        urls = 'participant' 

    if request.method == "POST":
        objectType.delete()
        messages.success(request, f"{types} Deleted successfully")
        return redirect(urls)  

    else:
        messages.error(request, f"Something went wrong")
         
    

    return redirect(urls)

