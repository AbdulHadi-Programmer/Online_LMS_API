from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators  import MinValueValidator, MaxValueValidator 

class CustomUser(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    bio = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=1000.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='course_img/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, editable=False) 

    


# Updated V1 -> V2
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=150)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.course.title})"    


class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    grade = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'course')
        

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

class Review(models.Model): 
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=250)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} → {self.course.title} ({self.rating}⭐)"

# V2
class Content(models.Model):
    content_types = (
        ('video', "Video"),
        ('text', "Text"),
        ('quiz', "Quiz"), 
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name= 'content')
    type = models.CharField(max_length=10, choices=content_types)
    order = models.PositiveIntegerField()

    # Flexible JSON field to store different structures 
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self): 
        return f'{self.type} in {self.lesson.title}'


from django.utils import timezone 
import datetime 

# V2
class ContentProgress(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="content_progress")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'content')
        ordering = ['-completed_at']

    def mark_complete(self): 
        self.is_completed = True 
        self.completed_at = timezone.now()
        self.save(update_fields=['is_completed', 'completed_at'])

    def __str__(self):
        status = "Completed" if self.is_completed else "Pending"
        return f"{self.student} "

# v2
class QuizSubmission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_submissions')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="quiz_submissions")
    answers = models.JSONField()
    score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)


