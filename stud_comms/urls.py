from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stud_comms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.login, name='login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comms-system/', include('core.urls')),
    url(r'^accounts/login/', views.login),
)

# Precaution; if debug is left on
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)