from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('game/', include('game.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('api/', include('api.urls')),
]
