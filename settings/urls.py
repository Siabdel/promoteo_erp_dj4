
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Liste des URL patterns
urlpatterns = [
    # Home page
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # Admin
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # Comments framework
    path('comments/', include('django_comments.urls')),
    path('comments-xtd/', include('django_comments_xtd.urls')),
    
    # Markdownx
    path('markdownx/', include('markdownx.urls')),

    # Third-party apps
    path('accounts/', include('allauth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

    # Core apps
    path('filebrowser/', include('core.filebrowser.urls')),
    path('widgets/', include('core.widgets.urls')),
    path('menus/', include('core.menus.urls')),
    path('taxonomy/', include('core.taxonomy.urls')),
    # path('auth/', include('core.auth.urls')),
    # path('registration/', include('core.registration.urls')),
    path('notifications/', include('core.notifications.urls')),
    path('calendar/', include('core.calendar.urls')),

    # Local apps (uncomment as needed)
    # path('todo/', include('todo.urls')),
    # path('addressing/', include('addressing.urls')),
    # path('partners/', include('partners.urls')),
    # path('documents/', include('documents.urls')),
    # path('products/', include('products.urls')),
    # path('stock/', include('stock.urls')),
    # path('hr/', include('hr.urls')),
    # path('sales/', include('sales.urls')),
    # path('projects/', include('projects.urls')),
    # path('knowledge/', include('knowledge.urls')),
]

# Ajout des fichiers statiques en mode debug
urlpatterns += staticfiles_urlpatterns()