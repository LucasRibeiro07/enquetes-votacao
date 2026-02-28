from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/enquetes/', permanent=False)),
    path('admin/', admin.site.urls),
    path('enquetes/', include('enquetes.urls')),  # inclui as urls do app
]