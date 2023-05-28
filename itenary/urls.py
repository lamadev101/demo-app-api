
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lay_travel.urls')),
    path('auth/',include('authentication.urls'))

]
