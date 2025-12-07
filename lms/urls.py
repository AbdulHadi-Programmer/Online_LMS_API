from django.urls import path
from .views import (
    RegisterAPIView,
    CustomTokenView,
    CourseAPIView, CourseDetailAPIView,
    LessonAPIView, LessonDetailAPIView,
    CategoryAPIView, CategoryDetailAPIView,
    EnrollmentAPIView, EnrollmentDetailAPIView,
    ReviewAPIView, ReviewDetailAPIView,
    GetAllUser, CurrentUserAPIView, UserDetailView, 
    ContentListCreateAPIView, ContentRetrieveUpdateDestroyAPIView,
    LesssonContentListCreateAPIView, CourseLessonListAPIView, 
    CourseFullDetailAPIView

)

urlpatterns = [
    # Auth
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/token/", CustomTokenView.as_view(), name="token_obtain_pair"),
    path("getall/", GetAllUser.as_view(), name=""),
    path("me/", CurrentUserAPIView.as_view(), name=""),
    path("getall/<int:pk>/", UserDetailView.as_view(), name=""),

    # Course
    path("courses/", CourseAPIView.as_view(), name="course_list"),
    path("courses/<int:pk>/", CourseDetailAPIView.as_view(), name="course_detail"),

    # Lesson
    path("lessons/", LessonAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson_detail"),

    # Category
    path("categories/", CategoryAPIView.as_view(), name="category_list"),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category_detail"),

    # Enrollment
    path("enrollments/", EnrollmentAPIView.as_view(), name="enrollment_list"),
    path("enrollments/<int:pk>/", EnrollmentDetailAPIView.as_view(), name="enrollment_detail"),

    # Review
    path("reviews/", ReviewAPIView.as_view(), name="review_list"),
    path("reviews/<int:pk>/", ReviewDetailAPIView.as_view(), name="review_detail"),

    # Content 
    path('content/', ContentListCreateAPIView.as_view(), name='content-list-create'),
    path('content/<int:id>/', ContentRetrieveUpdateDestroyAPIView.as_view(), name='content-get-update-delete'),

    # All lesson inside Content :
    path('lessons/<lesson_id>/content/', ContentListCreateAPIView.as_view(), name="specific-lesson-content"),
    # All lesson inside Content :
    path('courses/<course_id>/lessons/', CourseLessonListAPIView.as_view()),
    # All nested Data:
    path('course-data/<course_id>/', CourseFullDetailAPIView.as_view())
]

    