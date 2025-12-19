## Search, Order, Filter:
```sql
GET /lms/courses/?search=django    -- Search : django
GET /lms/courses/?category=2  -- Filter by category=2
GET /lms/courses/?ordering=-price --order by big prices
```

| Use case                        | Example URL                                     |
| ------------------------------- | ----------------------------------------------- |
| **All courses**                 | `/api/courses/`                                 |
| **Search for keyword “django”** | `/api/courses/?search=django`                   |
| **Filter by category id = 2**   | `/api/courses/?category=2`                      |
| **Filter and search combined**  | `/api/courses/?search=python&category=1`        |
| **Order by price ascending**    | `/api/courses/?ordering=price`                  |
| **Order by price descending**   | `/api/courses/?ordering=-price`                 |
| **Search + Order**              | `/api/courses/?search=web&ordering=-created_at` |


from lms.models import *
from django.utils import timezone

# ---------- USERS ----------
admin = CustomUser.objects.create_superuser(username='admin', password='admin123')
instructor1 = CustomUser.objects.create_user(username='sara', password='123', is_instructor=True)
instructor2 = CustomUser.objects.create_user(username='mark', password='123', is_instructor=True)
student1 = CustomUser.objects.create_user(username='alice', password='123', is_student=True)
student2 = CustomUser.objects.create_user(username='bob', password='123', is_student=True)
student3 = CustomUser.objects.create_user(username='charlie', password='123', is_student=True)

# ---------- CATEGORIES ----------
web_cat = Category.objects.create(name='Web Development', description='All about building websites')
data_cat = Category.objects.create(name='Data Science', description='Learn ML and data analysis')
mobile_cat = Category.objects.create(name='Mobile Apps', description='Android and iOS development')

# ---------- COURSES ----------
django_course = Course.objects.create(
    title='Django for Beginners',
    description='Full guide to Django framework',
    price=1500.00,
    category=web_cat,
    instructor=instructor1
)
react_course = Course.objects.create(
    title='React from Zero to Hero',
    description='Frontend UI with React.js',
    price=1200.00,
    category=web_cat,
    instructor=instructor1
)
python_ds_course = Course.objects.create(
    title='Python for Data Science',
    description='Hands-on with Pandas and Numpy',
    price=1800.00,
    category=data_cat,
    instructor=instructor2
)

# ---------- LESSONS ----------
Lesson.objects.create(course=django_course, title='Intro to Django', duration='10m', content='What is Django?', order=1)
Lesson.objects.create(course=django_course, title='Models & ORM', duration='20m', content='Defining models', order=2)
Lesson.objects.create(course=react_course, title='React Basics', duration='15m', content='Components and JSX', order=1)
Lesson.objects.create(course=python_ds_course, title='Numpy Arrays', duration='12m', content='Array manipulations', order=1)
Lesson.objects.create(course=python_ds_course, title='DataFrames', duration='18m', content='Intro to Pandas', order=2)

# ---------- ENROLLMENTS ----------
Enrollment.objects.create(student=student1, course=django_course, progress=50.0)
Enrollment.objects.create(student=student2, course=django_course, progress=80.0)
Enrollment.objects.create(student=student1, course=python_ds_course, progress=30.0)
Enrollment.objects.create(student=student3, course=react_course, progress=60.0)
Enrollment.objects.create(student=student2, course=react_course, progress=10.0)

# ---------- REVIEWS ----------
Review.objects.create(student=student1, course=django_course, rating=5, comment='Excellent course!', created_at=timezone.now())
Review.objects.create(student=student2, course=django_course, rating=4, comment='Very good, but could use more examples.', created_at=timezone.now())
Review.objects.create(student=student3, course=react_course, rating=5, comment='Perfect intro to React.', created_at=timezone.now())
Review.objects.create(student=student1, course=python_ds_course, rating=3, comment='Good start but too short.', created_at=timezone.now())


> Example Enrollment queries: 
- `?ordering=-progress` → descending by progress
- `?ordering=enrolled_at` → ascending by enrolled_at

## =====================================================================================================================================================================
### Practice Task:  (Task for 9 November 2025)

**1️⃣ LessonAPIView**
- **Search:** by title and content.
- **Filter:** by course_id and optionally duration.
- **Ordering:** by order or duration.

**2️⃣ ReviewAPIView**
Search: by comment or related course__title.
Filter: by rating and course.
Ordering: by created_at and rating.

**3️⃣ CategoryAPIView**
Search: by name and description.
Filter: no complex foreign key, but optionally filter by name.
Ordering: by name.

**4️⃣ LessonDetailAPIView / ReviewDetailAPIView / CategoryDetailAPIView**
- You don’t need search here, but optional ordering can be applied if returning nested lists (e.g., lessons of a course in `LessonDetailAPIView`).
**Extra Challenge (Optional)**
- Combine search + filter + ordering in LessonAPIView so you can do queries like:
`/api/lessons/?search=Django&course_id=1&ordering=-duration`
- Combine search + filter + ordering in ReviewAPIView so queries like:
`/api/reviews/?search=perfect&rating=5&ordering=-created_at`
work seamlessly.

