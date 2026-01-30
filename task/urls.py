from django.urls import path
from task.views import home,TaskCreate,participant,event,EventVeiw,category,Update,Delete_event,Loginhome,Rsvp,showRsvp
urlpatterns = [
    path('',home,name='Dashboards'),
    path("Dashboard/",Loginhome.as_view(), name="Loginhome"),
    path('form/',TaskCreate.as_view(),name='form'),
    path('participant/',participant.as_view(),name='participant'),
    path('event/',event.as_view(),name='event'),
    path('event/<int:id>/',EventVeiw.as_view(),name='view'),
    path('categories/', category.as_view(), name='category'),
    path('Update/<int:id>/', Update, name='update'),
    path('Delete/<int:id>/',Delete_event , name='delete'),

    path('RSVP/<int:id>/',Rsvp , name='rsvp_event'),
    path('event/show_event/',showRsvp, name='show_rsvp'),

    

]
