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
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0) 



# Updated V1 -> V2
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=150)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.course.title})"

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
    


class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    # progress = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], default=0.0)

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

# v2
class QuizSubmission(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='quiz_submissions')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="quiz_submissions")
    answers = models.JSONField()
    score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)

# V2
class ContentProgress(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="content_progress")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='progress')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'content')

