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
    CourseFullDetailAPIView, MyCoursesAPIView, GetSpecificUser,
    InstructorCoursesAPIView, ContentProgressPercentage, MarkCompleteAPIView,
    AssignGradeAPIView, CourseAnalyticsAPIView, 
)
from rest_framework_simplejwt.views import TokenRefreshView 

urlpatterns = [
    # Auth
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/token/", CustomTokenView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # name add kar diya
    path("users/", GetAllUser.as_view(), name="user_list"),  # better name
    path("me/", CurrentUserAPIView.as_view(), name="current_user"),
    path("users/<int:pk>/", GetSpecificUser.as_view(), name="user_detail"),

    # Course
    path("courses/", CourseAPIView.as_view(), name="course_list"),
    path("courses/<int:pk>/", CourseDetailAPIView.as_view(), name="course_detail"),

    # Lesson
    path("lessons/", LessonAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson_detail"),

    # Category
    path("categories/", CategoryAPIView.as_view(), name="category_list"),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category_detail"),

    # Enrollment   ----------------------
    path("enrollments/", EnrollmentAPIView.as_view(), name="enrollment_list_create"),
    path("enrollments/<int:pk>/", EnrollmentDetailAPIView.as_view(), name="enrollment_detail"),

    # Review   ------------------------
    path("reviews/", ReviewAPIView.as_view(), name="review_list_create"),
    path("reviews/<int:pk>/", ReviewDetailAPIView.as_view(), name="review_detail"),

    # Content --------
    path('content/', ContentListCreateAPIView.as_view(), name='content-list-create'),
    path('content/<int:id>/', ContentRetrieveUpdateDestroyAPIView.as_view(), name='content-detail'),

    # Specific lesson content
    path('lessons/<int:lesson_id>/content/', LesssonContentListCreateAPIView.as_view(), name="lesson-content"),  # typo fix: Lessson → Lesson

    # Lessons in course
    path('courses/<int:course_id>/lessons/', CourseLessonListAPIView.as_view(), name="course-lessons"),

    # Full nested course data  
    path('course-data/<int:course_id>/', CourseFullDetailAPIView.as_view(), name="course-full-data"),

    # Student specific
    path('enrollments/my-courses/', MyCoursesAPIView.as_view(), name='my-courses'),

    # Instructor specific   
    path('instructor-courses/', InstructorCoursesAPIView.as_view(), name='instructor-courses'),

    # Progress Tracking  ---> 2nd one progress check  
    path('progress/complete/<int:content_id>/', MarkCompleteAPIView.as_view(), name='mark-complete'),
    path('progress/course/<int:course_id>/', ContentProgressPercentage.as_view(), name='course-progress'),

    # Instructor tools  ---> 
    path('courses/<int:id>/grade/<int:student_id>/', AssignGradeAPIView.as_view(), name='assign-grade'),
    path('courses/<int:id>/analytics/', CourseAnalyticsAPIView.as_view(), name='course-analytics'),
]


# urlpatterns = [
#     # Auth
#     path("auth/register/", RegisterAPIView.as_view(), name="register"),
#     path("auth/token/", CustomTokenView.as_view(), name="token_obtain_pair"),
#     path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_obtain_pair"),
#     path("me/", CurrentUserAPIView.as_view(), name="current_user"),
#     path("users/", GetAllUser.as_view(), name="user_list"),
#     # path("getall/<int:pk>/", UserDetailView.as_view(), name=""),
#     path("users/<int:pk>/", GetSpecificUser.as_view(), name="user_detail"),
    

#     # Course
#     path("courses/", CourseAPIView.as_view(), name="course_list"),
#     path("courses/<int:pk>/", CourseDetailAPIView.as_view(), name="course_detail"),

#     # Lesson
#     path("lessons/", LessonAPIView.as_view(), name="lesson_list"),
#     path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson_detail"),

#     # Category
#     path("categories/", CategoryAPIView.as_view(), name="category_list"),
#     path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category_detail"),

#     # Enrollment
#     path("enrollments/", EnrollmentAPIView.as_view(), name="enrollment_list"),
#     path("enrollments/<int:pk>/", EnrollmentDetailAPIView.as_view(), name="enrollment_detail"),

#     # Review
#     path("reviews/", ReviewAPIView.as_view(), name="review_list"),
#     path("reviews/<int:pk>/", ReviewDetailAPIView.as_view(), name="review_detail"),

#     # Content 
#     path('content/', ContentListCreateAPIView.as_view(), name='content-list-create'),
#     path('content/<int:id>/', ContentRetrieveUpdateDestroyAPIView.as_view(), name='content-get-update-delete'),

#     # All lesson inside Content :
#     path('lessons/<lesson_id>/content/', ContentListCreateAPIView.as_view(), name="specific-lesson-content"),
#     # All lesson inside Content :
#     path('courses/<course_id>/lessons/', CourseLessonListAPIView.as_view()),
#     # All nested Data:
#     path('course-data/<course_id>/', CourseFullDetailAPIView.as_view()),
#     path('enrollments/my-courses/', MyCoursesAPIView.as_view(), name=''),
#     path('instructor-courses/', InstructorCoursesAPIView.as_view()),

#     ## Content Progress Tracking :
#     path('progress/complete/<content_id>/', MarkCompleteAPIView.as_view()),
#     path('progress/course/<course_id>/', ContentProgressPercentage.as_view()),

#     # Grade and Marks 
#     path('courses/<int:id>/grade/<int:student_id>/', AssignGradeAPIView.as_view(), name='assign-grade'),
#     path('courses/<int:id>/analytics/', CourseAnalyticsAPIView.as_view(), name="check-analytics"),
# ]

    