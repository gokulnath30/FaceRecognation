from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path("user_details",views.user_details,name="user_details"),
    
    path("ViewHistory", views.ViewHistory,name="ViewHistory"),

    path('homePage', views.index, name='index'),
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

