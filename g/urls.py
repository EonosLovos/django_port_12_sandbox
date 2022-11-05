from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('1/', include('a.urls')),
    path('admin/', admin.site.urls),
]