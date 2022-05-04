from django.urls import path
from .views import vegelist,marketprice,about,datasource
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',vegelist,name='index'),
    path('<int:pk>/marketprice',marketprice,name='marketprice'),
    path('about/',about,name='about'),
    path('datasource/',datasource,name='datasource'),
]+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)