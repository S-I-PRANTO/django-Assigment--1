from django.urls import path
from user.views import Sign_up,UserDash,Sign_in,Sign_out,activate_user,admin_dashboard,assign_role,create_group,group_list,Participent,OrganizeCategory,OrganizeEvent,Organize,AdminCategory,AdminEvent,AdminEventVeiw,OrganizeEventVeiw,dashboard_redirect,admin_UserList
from core.views import No_permission
from task.views import Loginhome
urlpatterns = [
    path('Dashboard/', dashboard_redirect, name='Dashboard'),
    path('user/',UserDash,name='user'),
    path('sign_up/',Sign_up,name='sign_up'),
    path('sign_in/',Sign_in,name='sign_in'),
    path('sign_out/',Sign_out,name='sign_out'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path("No_Permission/",No_permission ,name="no_permission"),

    path('showParticipant/',Participent ,name='adminParticipate'),

    path('organize/',Loginhome,name='organize'),
    path('organizeEvent/',OrganizeEvent,name='organizeEvent'),
    path('OrganizeEventView/<int:id>/',OrganizeEventVeiw,name='organizeview'),
    path('organizeCategory/',OrganizeCategory,name='organizeCategory'),

    path('Admindashboard/',Loginhome,name='adminDashboard'),
    path('AdminuserList/',admin_UserList,name='adminUserlist'),
    path('Adminassign-role/<int:user_id>/',assign_role ,name='assingRole'),
    path('Admincreate_group/',create_group ,name='createGroup'),
    path('Admingroup-list/',group_list ,name='groupList'),
    path('AdminEventView/<int:id>/',AdminEventVeiw,name='adminview'),
    path('AdminEvent/',AdminEvent,name='AdminEvent'),
    path('AdminCategory/',AdminCategory,name='AdminCategroy'),

]
