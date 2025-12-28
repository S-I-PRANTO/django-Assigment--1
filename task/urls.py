from django.urls import path
from task.views import home,form,participant,event,EventVeiw,category,Update,Delete_event
urlpatterns = [
    path('',home,name='Dashboard'),
    path('form/',form,name='form'),
    path('participant/',participant,name='participant'),
    path('event/',event,name='event'),
    path('event/<int:id>/',EventVeiw,name='view'),
    path('categories/', category, name='category'),
    path('Update/<int:id>/', Update, name='update'),
    path('Delete/<int:id>/',Delete_event , name='delete'),


]
