from django.urls import path
from task.views import home,form,participant,event,EventVeiw,category,Update,Delete_event,Loginhome,Rsvp,showRsvp
urlpatterns = [
    path('',home,name='Dashboards'),
    path("Dashboard/",Loginhome , name="Loginhome"),
    path('form/',form,name='form'),
    path('participant/',participant,name='participant'),
    path('event/',event,name='event'),
    path('event/<int:id>/',EventVeiw,name='view'),
    path('categories/', category, name='category'),
    path('Update/<int:id>/', Update, name='update'),
    path('Delete/<int:id>/',Delete_event , name='delete'),


    path('RSVP/<int:id>/',Rsvp , name='rsvp_event'),
    path('event/show_event/',showRsvp, name='show_rsvp'),

    

]
