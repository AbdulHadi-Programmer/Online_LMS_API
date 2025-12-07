from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Category, Enrollment, Review
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    CategorySerializer,
    EnrollmentSerializer,
    ReviewSerializer,
    RegisterSerializer,
)
from .permissions import (
    IsInstructorOnly,
    IsCourseInstructorOrReadOnly,
    IsLessonInstructorOrReadOnly,
    IsEnrolledStudentForReview,
    IsReviewOwnerOrReadOnly

)
from .models import CustomUser
from .serializers import UserSerializer, CourseFullSerializer
# JWT Custom Token View
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


# =========================================================
# AUTH
# =========================================================
from rest_framework.permissions import AllowAny

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllUser(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)

# =========================================================
# COURSE CRUD
# =========================================================

class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInstructorOnly]

    def get(self, request):
        courses = Course.objects.all()

        # SEARCH
        search = request.query_params.get("search")
        if search:
            courses = courses.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(category__name__icontains=search)
            )

        # FILTER
        category = request.query_params.get("category")
        if category:
            courses = courses.filter(category_id=category)

        # ORDERING
        ordering = request.query_params.get("ordering")
        allowed = ["title", "created_at", "price"]
        if ordering and ordering.lstrip("-") in allowed:
            courses = courses.order_by(ordering)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCourseInstructorOrReadOnly]

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =========================================================
# LESSON CRUD
# =========================================================

class LessonAPIView(APIView):
    permission_classes = [IsAuthenticated, IsLessonInstructorOrReadOnly]

    def get(self, request):
        lessons = Lesson.objects.all()

        search = request.query_params.get("search")
        if search:
            lessons = lessons.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        course = request.query_params.get("course")
        if course:
            lessons = lessons.filter(course_id=course)

        ordering = request.query_params.get("ordering")
        allowed = ["order", "duration"]
        if ordering and ordering.lstrip("-") in allowed:
            lessons = lessons.order_by(ordering)

        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsLessonInstructorOrReadOnly]

    def get(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def put(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lesson = get_object_or_404(Lesson, pk=pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =========================================================
# CATEGORY CRUD
# =========================================================

class CategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =========================================================
# ENROLLMENT CRUD
# =========================================================
from .permissions import IsStudentEnrollingSelf, IsInstructorManagingEnrollment
class EnrollmentAPIView(APIView):
    permission_classes = [IsStudentEnrollingSelf | IsInstructorManagingEnrollment]
    def get(self, request):
        queryset = Enrollment.objects.all()

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(student__username__icontains=search)
                | Q(course__title__icontains=search)
            )

        course = request.query_params.get("course")
        if course:
            queryset = queryset.filter(course_id=course)

        progress = request.query_params.get("progress")
        if progress:
            queryset = queryset.filter(progress__gte=progress)

        ordering = request.query_params.get("ordering")
        allowed = ["enrolled_at", "progress"]
        if ordering and ordering.lstrip("-") in allowed:
            queryset = queryset.order_by(ordering)

        serializer = EnrollmentSerializer(queryset, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = EnrollmentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()  
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        user = request.user 
        data = request.data.copy()  # copy so we can modify 
        
        # Student self-enrollment 
        if user.is_student:
            # enforce that student can only enroll themselves 
            data['student'] = user.id
            serializer = EnrollmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(student=user)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        
        # Instructor Enrolling in a student 
        elif user.is_instructor:
            course_id = data.get('course')
            student_id = data.get('student')

            # Make sure the instructor owns the course
            course = get_object_or_404(Course, id=course_id)
            if course.instructor != user:
                return Response({"detail": "You can only enroll students in your own courses."}, status=403)

            serializer = EnrollmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()  # student comes from request.data['student']
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        else:
            return Response({"detail": "Unauthorized"}, status=403)


class EnrollmentDetailAPIView(APIView):
    def get(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    def put(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk)
        serializer = EnrollmentSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk)
        serializer = EnrollmentSerializer(enrollment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# =========================================================
# REVIEW CRUD
# =========================================================
from rest_framework.permissions import AllowAny

class ReviewAPIView(APIView):
    # Simplify permissions: POST requires authentication, others are open.
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Add enrollment check here before serializing
        user = request.user
        course_id = request.data.get("course")

        # Assuming 'Enrollment' model is correct as provided in your permission class logic
        if not course_id or not Enrollment.objects.filter(student=user, course_id=course_id).exists():
            return Response(
                {"detail": "You must be an enrolled student in this course to leave a review."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(student=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Review Detail APIView :
class ReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsReviewOwnerOrReadOnly]

    def get_object(self, pk):
        obj = get_object_or_404(Review, pk=pk)
        self.check_object_permissions(self.request, obj)  # enforce owner check
        return obj

    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]  # user must be logged in

    def get(self, request):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "is_student": user.is_student,
            "is_instructor": user.is_instructor,
        }
        return Response(data)
    
from django.http import Http404

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
        
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from .models import Content, ContentProgress, QuizSubmission
from .serializers import ContentProgressSerializer, ContentSerializer, QuizSubmissionSerializer
from .permissions import IsQuizOwnerOrReadOnly, IsEnrolledInCourse, CanSubmitQuizOnce 
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 

class QuizListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        quizzes = Content.objects.filter(type="quiz")
        serializer = ContentSerializer(quizzes, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_instructor:
            return Response({"error": "Only Instructor can create quizzes"}, status=403)
        
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(instructor = request.user,type="quiz") # force type
            return Response(serializer.errors , status=400)
        return Response(serializer.errors, status=400)

class QuizRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsQuizOwnerOrReadOnly, IsEnrolledInCourse ]

    def get_object(self, id):
        quiz = get_object_or_404(Content, id=id, type='quiz')
        self.check_object_permissions(self.request, quiz)

    def get(self, request, id):
        quiz = self.get_object(id)
        serializer = ContentSerializer(quiz)
        return Response(serializer.data)

    def put(self, request, id):
        quiz = self.get_object(id)
        serializer = ContentSerializer(quiz, data=request.data, partial =False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)

    def patch(self, request, id):
        quiz = self.get_object(id)
        serializer = ContentSerializer(quiz, data=request.data, partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)

    def delete(self, request, id):
        quiz = self.get_object(id)
        quiz.delete()
        return Response({"message": "Deleted"}, status=204)


class QuizSubmitAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEnrolledInCourse, CanSubmitQuizOnce]

    def post(self, request, id):
        quiz = get_object_or_404(Content, id=id, type="quiz")
        self.check_object_permissions(request, quiz)

        serializer = QuizSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Extract answers and score them
        score = self.calculate_score(quiz, serializer.validated_data["answers"])

        submission = serializer.save(
            student=request.user,
            content=quiz,
            score=score
        )

        return Response({
            "message": "Quiz Submitted Successfully",
            "score": score, 
            "submission_id": submission.id 
        }, status=201)

    def calculate_score(self, quiz, answers):
        questions = quiz.data.get("questions", [])
        if not questions:
            return 0
        
        correct = sum(1 for i, q in enumerate(questions) if answers.get(str(i)) == q.get("answer"))

        return round((correct / len(questions)) * 100, 2)


# lesson
# type
# order - Positive Integer
# data - jsonfield
# ==========================
#       Content CRUD       :
# ==========================
class ContentListCreateAPIView(APIView):
    def get(self, request, lesson_id=None):
        if lesson_id:
            content = Content.objects.filter(lesson_id=lesson_id)
        else:
            content = Content.objects.all()

        # content = Content.objects.all()
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ContentRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, id):
        content = get_object_or_404(Content, id=id)
        serializer = ContentSerializer(content)
        return Response(serializer.data)
    
    def put(self, request, id):
        quiz = get_object_or_404(Content, id=id)
        serializer = ContentSerializer(quiz, data=request.data, partial =False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)
    
    def patch(self, request, id):
        quiz = get_object_or_404(Content, id=id)
        serializer = ContentSerializer(quiz, data=request.data, partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = 400)
    
    def delete(self, request, id):
        quiz = get_object_or_404(Content, id=id)
        quiz.delete()
        return Response({"message": "Deleted"}, status=204)



### Content Specific V2 Features :
# Content inside lessson
class LesssonContentListCreateAPIView(APIView):
    def get(self, request, lesson_id):
        qs = Content.objects.filter(lesson_id=lesson_id)
        serializer = ContentSerializer(qs, many=True)
        return Response(serializer.data)

# Lesson inside Courses
class CourseLessonListAPIView(APIView):
    def get(self, request, course_id):
        qs = Lesson.objects.filter(course=course_id)
        serializer = LessonSerializer(qs, many=True)
        return Response(serializer.data)


# All data course -> lesson -> content :
class CourseFullDetailAPIView(APIView):
    def get(self, request, course_id):
        course = get_object_or_404(Course.objects.prefetch_related("lessons__content"), id=course_id)
        serializer = CourseFullSerializer(course)
        return Response(serializer.data)
    