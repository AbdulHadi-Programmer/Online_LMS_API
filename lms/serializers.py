from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Category, Course, Lesson, Enrollment, Review


# -----------------------
# Registration: creates user only
# -----------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "is_student", "is_instructor"]

    def validate(self, data):
        # Prevent selecting both roles
        if data.get("is_student") and data.get("is_instructor"):
            raise serializers.ValidationError("User cannot be both student and instructor.")

        # Validate password strength (raises ValidationError if invalid)
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


# -----------------------
# User representation (no password, used for returning user info)
# -----------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "bio", "profile_image", "is_student", "is_instructor"]
        read_only_fields = ["id", "is_student", "is_instructor"]

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return fields 
        if request.user.id == self.instance :
            return fields 
        return fields 
    

# -----------------------
# Custom JWT payload: include role flags so frontend knows who the user is
# -----------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "is_student": self.user.is_student,
            "is_instructor": self.user.is_instructor,
        }

        return data


# -----------------------
# Category
# -----------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# -----------------------
# Course
# -----------------------
class CourseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    instructor_name = serializers.CharField(source="instructor.username", read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "description", "price",
            "category", "category_name",
            "instructor", "instructor_name",
            "thumbnail", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


# -----------------------
# Lesson
# -----------------------
class LessonSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "course", "course_name", "title", "order"]
        


# -----------------------
# Enrollment
# -----------------------
class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.username", read_only=True)
    course_name = serializers.CharField(source="course.title", read_only=True)
    instructor = serializers.CharField(source='course.instructor.username', read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "student", "student_name", "course", "course_name", 'instructor', 'is_active', "enrolled_at" ]
        read_only_fields = ["enrolled_at", 'is_active']



# -------------------------------------------------------
# Review Serializer (auto-updates course average rating)
# -------------------------------------------------------
class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.username", read_only=True)
    course_name = serializers.CharField(source="course.title", read_only=True)

    # Add this field to show the calculated average rating of the course
    course_average_rating = serializers.DecimalField(
        source="course.average_rating", 
        max_digits=3, 
        decimal_places=1, 
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id', 'student', 'student_name', 'course', 'course_name', 
            'course_average_rating',
            'rating', 'comment', 'created_at'
        ]

    def create(self, validated_data):
        review = super().create(validated_data)
        self.update_course_rating(review.course)
        return review

    def update(self, instance, validated_data):
        review = super().update(instance, validated_data)
        self.update_course_rating(review.course)
        return review

    def update_course_rating(self, course):
        from django.db.models import Avg
        avg_rating = course.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        course.average_rating = round(avg_rating, 1)
        course.save()


## Version 2 :
from .models import QuizSubmission, Content, ContentProgress
class ContentSerializer(serializers.ModelSerializer):
    lesson_name = serializers.CharField(source='lesson.title', read_only=True)
    course_name = serializers.CharField(source='lesson.course.title', read_only=True)
    
    def get_content_title(self, obj):
        return obj.content.data.get('title') or f"{obj.content.type.capitalize()} Content"
    
    class Meta:
        model = Content
        fields = ["id", "lesson", "lesson_name", "course_name","type", "order", "data", "created_at"]        
        read_only_fields = ["id", "created_at"]


# -----------------------------
#  Quiz Submission Serializer 
# -----------------------------
class QuizSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.username", read_only=True)

    class Meta:
        model = QuizSubmission
        fields = ["id", "student", "student_name", "content", "answers", "score", "submitted_at"]
        read_only_fields = ["score", "submitted_at"]


## Nested Data Serializer :
class LessonWithContentSerializer(serializers.ModelSerializer):
    content = ContentSerializer(many=True, read_only=True)  # this can import 'content field' into lessons 
    class Meta:
        model = Lesson 
        fields= ["id", "title", "order", "content"]


class CourseFullSerializer(serializers.ModelSerializer):
    lessons= LessonWithContentSerializer(many=True, read_only=True)  # this can import the above data into the course
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    category_name= serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "description","price", "thumbnail", "category", "category_name", "instructor", "instructor_name", "average_rating", "created_at", "updated_at", "lessons" ]
        read_only_fields = ["id", "created_at", "updated_at", "average_rating"]


# =========================================
#   Content Progress 
# =========================================
class ContentProgressSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    content_title = serializers.SerializerMethodField()

    def get_content_title(self, obj):
        return obj.content.data.get('title') or f"{obj.content.type.capitalize()} Content"

    class Meta:
        model = ContentProgress 
        fields = ["id", "student_name", "student", "content", "content_title", "is_completed", "completed_at"]        

        
