from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
    path('error/', TemplateView.as_view(template_name='error.html'), name='error'),
    path('', include('organizer.urls')),
    path('calendar/', include('appcalendar.urls')),
    path('user/', include('appuser.urls'))
]
