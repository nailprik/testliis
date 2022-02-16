from rest_framework.routers import SimpleRouter

from .views import ArticleViewSet, RegisterViewSet

router = SimpleRouter()

router.register('register', RegisterViewSet, basename='register')
router.register('article', ArticleViewSet, basename='article')

urlpatterns = []

urlpatterns += router.urls