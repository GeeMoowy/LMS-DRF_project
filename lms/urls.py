from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.views import (CourseViewSet, LessonListApiView, LessonUpdateApiView, LessonCreateApiView, LessonDestroyApiView,
                       LessonRetrieveApiView, SubscriptionAPIView)
from lms.apps import LmsConfig


app_name = LmsConfig.name

router = SimpleRouter()
router.register('courses', CourseViewSet, basename='courses')

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/destroy/", LessonDestroyApiView.as_view(), name="lessons_destroy"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),

]

urlpatterns += router.urls
