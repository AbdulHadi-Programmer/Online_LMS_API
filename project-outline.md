# 2 November 2025:
### 🧩 Project: Online Learning Platform API (Full Backend Plan)
1. **🌐 Project Overview**
You’re building a backend API for a platform where:
- Instructors can create and manage courses.
- Students can enroll in and view courses.
- Admins manage users and approve instructors.

You’ll create **separate APIs** for:
- Authentication (Register/Login/Logout)
- Course Management
- Lesson Management
- Enrollment & Progress Tracking
- Review & Rating System
- File Upload (course thumbnails, PDFs, or videos)
- Search, Filtering, and Pagination

2. **👤 User Roles & Permissions**

 | Role           | Description                      | Permissions                              |
| -------------- | -------------------------------- | ---------------------------------------- |
| **Admin**      | Superuser who manages everything | Full access to all models                |
| **Instructor** | Creates courses, uploads content | CRUD on own courses & lessons            |
| **Student**    | Enrolls and watches courses      | Can read all courses, create enrollments |
| **Anonymous**  | Not logged in                    | Read-only (list of public courses)       |

3. **🧱 Core Models (Conceptual Design)**
**1️⃣ User**
- Based on Custom User model (AbstractUser).
- Fields:
    - `username`, `email`, `password`
    - `is_instructor` (Boolean)
    - `is_student` (Boolean)
    - `bio`, `profile_image` (optional)
- Relationship: One-to-One with InstructorProfile or StudentProfile (optional advanced feature).

**2️⃣ Category**
- Example: “Programming”, “Design”, “Business”
- Fields:
  * name (unique)
  * description

**3️⃣ Course**
- Owned by Instructor.
- Fields:
  * title
  * description
  * price
  * category (ForeignKey → Category)
  * instructor (ForeignKey → User)
  * thumbnail (Image upload)
  * created_at, updated_at

- Permissions:
  * Only Instructor who created it can update/delete.
  * Students can only view or enroll.


**4️⃣ Lesson**
- Belongs to a Course.
- Fields:
  * course (ForeignKey → Course)
  * title
  * video (File upload)
  * duration
  * content (text/markdown)
  * order (integer to sort lessons)

- Permission:
  * Instructor can create/edit lessons for own course.
  * Student can view lessons of enrolled courses only.


**5️⃣ Enrollment**
- Tracks which students are enrolled in which course.
- Fields:
  * student (ForeignKey → User)
  * course (ForeignKey → Course)
  * enrolled_on (DateTime)
  * progress (FloatField, e.g., 0–100%)

- Permission:
  * Students can only create their own enrollment.
  * Instructor can view enrolled students.

**6️⃣ Review**
- Students leave reviews after completing a course.
- Fields:
  * student
  * course
  * rating (1–5)
  * comment
  * created_at

- Permission:
  * Only enrolled students can post reviews. 


### 🔐 4. Authentication Plan (JWT)
You’ll use SimpleJWT for token-based authentication:
`/api/register/` → Create new account (student or instructor)
`/api/login/` → Get access + refresh tokens
`/api/logout/` → Blacklist refresh token
`/api/token/refresh/` → Get new access token
`/api/profile/` → View current user details

You can also add optional:
`/api/change-password/`
`/api/update-profile/`


### ⚙️ 5. Course & Lesson APIs
**Public Endpoints**
- `GET /api/courses/` → List all courses (paginated)
- `GET /api/courses/?search=python` → Search courses
- `GET /api/courses/?category=design` → Filter by category
- `GET /api/courses/{id}/` → Retrieve course detail with instructor & lessons info

**Instructor Endpoints**
- `POST /api/courses/` → Create new course
- `PUT/PATCH /api/courses/{id}/` → Update own course
- `DELETE /api/courses/{id}/` → Delete own course
- `POST /api/lessons/` → Add lessons to own course
- `PUT/PATCH /api/lessons/{id}/` → Edit lesson content
- `DELETE /api/lessons/{id}/` → Delete lesson

**Student Endpoints**
- `POST /api/enroll/{course_id}/` → Enroll in a course
- `GET /api/my-courses/` → List enrolled courses
- `GET /api/my-progress/` → Track learning progress
- `POST /api/reviews/` → Post review after completing

### 📄 6. File Uploads
Use DRF’s built-in file handling for:
- Course thumbnails (images)
- Lesson videos (media files)
- Profile pictures

Settings needed:
- MEDIA_URL and MEDIA_ROOT
- Ensure file uploads are authenticated for instructors only.

### 🔍 7. Filtering, Search, and Ordering
Use DRF’s SearchFilter, OrderingFilter, and DjangoFilterBackend.
Example Filters:
`/api/courses/?search=python`
`/api/courses/?category=design`
`/api/courses/?ordering=price`
`/api/courses/?ordering=-created_at`


### 📊 8. Pagination Plan
Use PageNumberPagination with:
- Default limit: 5 or 10 items per page
- Example:
  - `/api/courses/?page=2`


### 🛡️ 9. Permissions Plan
| Resource       | Who can access                 | Type of Permission |
| -------------- | ------------------------------ | ------------------ |
| Register/Login | Everyone                       | AllowAny           |
| Course List    | Everyone                       | AllowAny           |
| Course Create  | Instructor only                | IsInstructor       |
| Lesson CRUD    | Only Instructor of that course | CustomPermission   |
| Enrollment     | Only Authenticated Students    | IsAuthenticated    |
| Review         | Enrolled Students              | CustomPermission   |
| Profile        | Authenticated User             | IsAuthenticated    |

You’ll write custom permission classes like:
- `IsInstructor`
- `IsOwnerOrReadOnly`
- `IsEnrolledStudent`


