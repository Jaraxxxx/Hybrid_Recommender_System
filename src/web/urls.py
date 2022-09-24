from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/',views.detail ,name='detail'),
    path('signup/',views.signUp,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('recommend/',views.recommend,name='recommend'),
]
urlpatterns += staticfiles_urlpatterns()