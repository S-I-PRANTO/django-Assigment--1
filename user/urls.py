from django.urls import path
from user.views import Sign_up,Sign_in,Sign_out,UserDash,activate_user,admin_dashboard,assign_role,create_group,group_list,Participent,OrganizeCategory,OrganizeEvent,Organize,AdminCategory,AdminEvents,AdminEventVeiw,OrganizeEventVeiw,dashboard_redirect,CustomProfileView,admin_UserList,CustomPasswordReset,EditProfileView,ChangePasswords,CustomPasswordResetConfirmView
from core.views import No_permission
from task.views import Loginhome
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
urlpatterns = [
    path('Dashboard/', dashboard_redirect, name='Dashboard'),
    path('user/',UserDash.as_view(),name='user'),
    path('sign_up/',Sign_up,name='sign_up'),
    path('sign_in/',Sign_in,name='sign_in'),
    path('sign_out/',Sign_out,name='sign_out'),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path("No_Permission/",No_permission ,name="no_permission"),

    path('showParticipant/',Participent ,name='adminParticipate'),

    path('organize/',Loginhome.as_view(),name='organize'),


    path('organizeEvent/',OrganizeEvent,name='organizeEvent'),
    path('OrganizeEventView/<int:id>/',OrganizeEventVeiw,name='organizeview'),
    path('organizeCategory/',OrganizeCategory,name='organizeCategory'),

    path('Admindashboard/',Loginhome.as_view(),name='adminDashboard'),


    path('AdminuserList/',admin_UserList,name='adminUserlist'),

    path('Adminassign-role/<int:user_id>/',assign_role.as_view() ,name='assingRole'),

    path('Admincreate_group/',create_group ,name='createGroup'),

    path('Admingroup-list/',group_list ,name='groupList'),

    path('AdminEventView/<int:id>/',AdminEventVeiw.as_view(),name='adminview'),
    path('AdminEvent/',AdminEvents.as_view(),name='AdminEvent'),
    path('AdminCategory/',AdminCategory,name='AdminCategroy'),


    path('profile/',CustomProfileView.as_view(),name='profile'),
    path('password_change/',ChangePasswords.as_view(),name='changePassword'),
    path('password_change/done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),

    path('password_reset/',CustomPasswordReset.as_view(),name='passwordReset'),
    path('password_reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('edit_profile/',EditProfileView.as_view(),name='edit_profile')



]
