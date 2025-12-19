from rest_framework.permissions import BasePermission, SAFE_METHODS
from lms.models import Enrollment
from lms.models import *

# ==========================================================
# COURSE PERMISSIONS
# ==========================================================

class IsCourseInstructorOrReadOnly(BasePermission):
    """
    Only the instructor who owns the course can edit/delete it.
    Everyone else (students or visitors) can only read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.instructor == request.user  # CORRECT FIELD

class IsInstructorOnly(BasePermission):
    """
    Only instructors can create courses or lessons.
    """
    def has_permission(self, request, view):
        # Allow any authenticated user to perform GET, HEAD, or OPTIONS
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        
        return bool(request.user and request.user.is_authenticated and request.user.is_instructor )


# ==========================================================
# LESSON PERMISSIONS
# ==========================================================

class IsLessonInstructorOrReadOnly(BasePermission):
    """
    Only the instructor who owns the course can modify/delete lessons.
    Everyone else can only view.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # FIX: you had obj.course.intructor (typo)
        return obj.course.instructor == request.user


class IsLessonOwnerOrReadOnly(BasePermission):
    """
    Same as above — but your old version was broken.
    Included ONLY because you referenced it, but cleaned properly.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.course.instructor == request.user


# ==========================================================
# STUDENT PERMISSIONS
# ==========================================================

class IsStudentOnly(BasePermission):
    """
    Only students can perform student-only actions.
    """
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.is_student
        )


# ==========================================================
# REVIEW PERMISSIONS
# ==========================================================

class IsEnrolledStudentForReview(BasePermission):
    """
    A student can leave a review ONLY if:
    - they are authenticated
    - they are a student
    - they are enrolled in the course they are reviewing
    """

    def has_permission(self, request, view):
        # GET, PATCH, DELETE are allowed — handled by object checks
        if request.method != "POST":
            return True

        user = request.user
        if not user.is_authenticated or not user.is_student:
            return False

        course_id = request.data.get("course")
        if not course_id:
            return False

        return Enrollment.objects.filter(
            student=user,
            course_id=course_id
        ).exists()


# ==========================================================
# ADMIN PERMISSIONS
# ==========================================================

class IsAdminOrReadOnly(BasePermission):
    """
    Only admin users can modify.
    Anyone can view.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_staff)


class IsReviewOwnerOrReadOnly(BasePermission):
    """
    Only the review creator can edit or delete their review
    Others can only read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True 
        return obj.student == request.user 
    
# ==========================
# Enrollment Permission 
# ==========================

class IsStudentEnrollingSelf(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student

class InstructorManagingEnrollment(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.is_instructor :
            return False
        if request.method in SAFE_METHODS:
            return True 
        course_id = request.data.get('course')
        if not course_id :
            return False 
        return Course.objects.filter(id=course_id, instructor=request.user).exists()

# ==============================
#   Quiz Permission 
# ==============================
# permissions.py
from .models import QuizSubmission

class IsQuizOwnerOrReadOnly(BasePermission):
    """
    Only Instructor can access this:
    1. Only the Owner can edit or delete 
    2. Every other instructor can only see others quiz
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user.is_authenticated and request.user.is_instructor)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, 'instructor', None) == request.user

class IsEnrolledInCourse(BasePermission):
    """
    Student can only access the enrolled course quizzes 
    Everyone else can view it only (GET)
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_instructor:
            return True
        if not request.user.is_authenticated:
            return False
            
        course = obj.lesson.course if hasattr(obj, 'lesson') else obj.course
        return Enrollment.objects.filter(student=request.user, course=course).exists()

class CanSubmitQuizOnce(BasePermission):
    """
    Student can submit the quiz at first attempt only
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_student:
            return False
        return not QuizSubmission.objects.filter(quiz_content=obj, student=request.user).exists()

# IsCourseInstructorOrReadOnly, IsInstructorOnly, IsLessonInstructorOrReadOnly, IsLessonOwnerOrReadOnly, IsStudentOnly, IsEnrolledStudentForReview, IsAdminOrReadOnly, IsReviewOwnerOrReadOnly, IsStudentEnrollingSelf, InstructorManagingEnrollment, IsQuizOwnerOrReadOnly, IsEnrolledInCourse, CanSubmitQuizOnce 