from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'user_auth'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('my_page/<int:pk>/', views.MyPage.as_view(), name='my_page'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('signup_done/', views.SignupDone.as_view(), name='signup_done'),
    path('user_update/<int:pk>', views.UserUpdate.as_view(), name='user_update'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    # path('password_chage_done', auth_views.PasswordChangeDoneView.as_view(template_name="user_auth/password_change_done.html"), name='password_change_done')

]
