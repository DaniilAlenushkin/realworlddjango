"""realworlddjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from django.conf.urls import url
from django.views.static import serve

from .yasg import urlpatterns as doc_url

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Frontend URLs
urlpatterns += [
    path('', include('main.urls')),
    path('events/', include('events.urls')),
    path('accounts/', include('accounts.urls')),
    path('mail/', include('mail.urls')),
    path('allauth/accounts/', include('allauth.urls')),
]
# API URLs
urlpatterns += [
    path('api/events/', include('events.urls_api')),
    path('api/mail/', include('mail.urls_api')),
]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

urlpatterns += doc_url

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
