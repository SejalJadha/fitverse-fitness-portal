from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.handlelogin,name='handlelogin'),
    path('logout/',views.handlelogout,name='logout'),
    path('contact',views.contact,name='contact'),
    path('enroll/',views.enroll,name='enroll'),
    path('profile/',views.profile,name="profile"),
     path('gallery',views.gallery,name="gallery"),
    path('attendance',views.attendance,name="attendance"),

]
