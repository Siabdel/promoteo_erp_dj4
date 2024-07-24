
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
import importlib

urlpatterns = [
    # Home page.
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # Admin.
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # Comments framework.
    path('comments/', include('django_comments.urls')),
]

urlpatterns += staticfiles_urlpatterns()

LOADING = False

def autodiscover():
    """ Auto discover urls of installed applications.
    """
    global LOADING
    if LOADING:
        return

    LOADING = True

    for app in settings.INSTALLED_APPS:
        if app.startswith('django') or app == '.core':
            continue

        # Step 1: find out the app's __path__.
        try:
            app_module = importlib.import_module(app)
            app_path = app_module.__path__
        except AttributeError:
            continue

        # Step 2: use importlib.util.find_spec to find the app's urls.py.
        try:
            importlib.util.find_spec('urls', app_path)
        except ImportError:
            continue

        # Step 3: return the app's url patterns.
        global urlpatterns
        urlpatterns.append(path('', include(f'{app}.urls')))

    LOADING = False

# Call autodiscover to load URLs from installed apps
autodiscover()  