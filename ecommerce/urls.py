from django.contrib import admin
from django.urls import path, include  # ✅ Make sure 'include' is imported
 # ✅ Import static to serve media files in development
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # ✅ Include the store app's URLs correctly
] # ✅ Serve media files in development
