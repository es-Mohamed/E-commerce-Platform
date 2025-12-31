"""
URL configuration for puddle project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.http import HttpResponse


# # Admin branding
# admin.site.site_header = "Puddle Admin (Mohamed Mady)"
# admin.site.site_title = "Puddle Portal"
# admin.site.index_title = "Welcome to the Experimental Demo"


# def landing_view(request):
#         html = '''
#         <!doctype html>
#         <html lang="en">
#         <head>
#             <meta charset="utf-8">
#             <meta name="viewport" content="width=device-width,initial-scale=1">
#             <title>Auto parts API</title>
#             <style>
#                 :root { color-scheme: dark; }
#                 body { background:#0b1220; color:#e6eef8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; height:100vh; margin:0; display:flex; align-items:center; justify-content:center; }
#                 .card { text-align:center; padding:2rem; border-radius:12px; background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); box-shadow: 0 6px 24px rgba(2,6,23,0.6); max-width:720px; }
#                 h1 { margin:0 0 0.5rem 0; font-size:2rem; }
#                 p { margin:0.25rem 0; color:#9fb2d6 }
#                 footer { margin-top:1.25rem; font-size:0.85rem; color:#7f98bf }
#             </style>
#         </head>
#         <body>
#             <div class="card">
#                 <h1>Auto parts API</h1>
#                 <p>Experimental Demo Version </p>
#                 <footer>Powered by Mohamed Mady</footer>
#             </div>
#         </body>
#         </html>
#         '''
#         return HttpResponse(html)


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('set-language/', set_language, name='set_language'),
] + i18n_patterns(
    path('admin/', admin.site.urls),
    # path('', landing_view),
    path('items/', include('items.urls')),
    path('inbox/', include('conversation.urls')),
    path('Dashboard/', include('Dashboard.urls')),
    path('cart/', include('cart.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)