from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf.urls.static import static
from playlistapi.views import UserView, TagView, EpisodeView, FriendView, PlaylistView
from . import settings

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"tags", TagView, "tag")
router.register(r"playlists", PlaylistView, "playlist")
router.register(r"friends", FriendView, "friend")
router.register(r"episodes", EpisodeView, "episode")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login', UserView.as_view({"post": "login_user"}), name="login"),
    path('register', UserView.as_view({'post': 'register_account'}), name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
