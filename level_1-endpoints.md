## 23 November 2025:
### Level 1 All Endpoint:

### 🔵 AUTH ENDPOINTS

| Method | Endpoint                  | Description                                    |
| ------ | ------------------------- | ---------------------------------------------- |
| POST   | `/lms/auth/register/`     | Create a new user (student or instructor)      |
| POST   | `/lms/auth/token/`        | Get JWT access + refresh tokens with user info |
| POST   | `/lms/auth/refresh/`      | Refresh JWT token                              |
| GET    | `/lms/auth/me/`           | Give Current User Info                         |
| GET    | `/lms/auth/getall/`       | Give All User Info                             |


### 🟣 COURSE ENDPOINTS
| Method      | Endpoint                      | Permission             | Description            |
| ----------- | ----------------------------- | ---------------------- | ---------------------- |
| GET         | `/lms/courses/`               | Anyone                 | List all courses       |
| POST        | `/lms/courses/`               | Instructor only        | Create a course        |
| GET         | `/lms/courses/<id>/`          | Anyone                 | Retrieve one course    |
| PUT / PATCH | `/lms/courses/<id>/`          | Only course instructor | Update course          |
| DELETE      | `/lms/courses/<id>/`          | Only course instructor | Delete course          |
### THis below should be created first =:=:=:=:=:= 
| GET         | `/lms/courses/<id>/students/` | Instructor only        | View enrolled students |


### 🟠 LESSON ENDPOINTS
| Method      | Endpoint             | Permission                        |
| ----------- | -------------------- | --------------------------------- |
| GET         | `/lms/lessons/`      | Anyone                            |
| POST        | `/lms/lessons/`      | Instructor only — must own course |
| GET         | `/lms/lessons/<id>/` | Anyone                            |
| PUT / PATCH | `/lms/lessons/<id>/` | Only the course owner instructor  |
| DELETE      | `/lms/lessons/<id>/` | Only the course owner instructor  |

### 🟢 ENROLLMENT ENDPOINTS
| Method | Endpoint                 | Permission               |
| ------ | ------------------------ | ------------------------ |
| GET    | `/lms/enrollments/`      | Instructor only OR Admin |
| POST   | `/lms/enrollments/`      | Students only            |
| GET    | `/lms/enrollments/<id>/` | Only related student     |
| DELETE | `/lms/enrollments/<id>/` | Only related student     |


### 🟡 REVIEW ENDPOINTS
| Method               | Endpoint             | Permission                                |
| -------------------- | -------------------- | ----------------------------------------- |
| GET                  | `/lms/reviews/`      | Anyone                                    |
| POST                 | `/lms/reviews/`      | Enrolled student only                     |
| GET                  | `/lms/reviews/<id>/` | Anyone                                    |
| PUT / PATCH / DELETE | `/lms/reviews/<id>/` | owner-only editing                        |


#### ⚡ Summary of what your system supports right now
✔ JWT Authentication
✔ User registration
✔ Role-based permissions
✔ Create/update/delete courses (instructors only)
✔ Create/update/delete lessons (instructors only)
✔ Student enrollments
✔ Course reviews
✔ Instructor-only or student-only actions
✔ API split by resources
You’ve basically built the skeleton of a full learning platform.

## Update to make for Version 2 :
<!-- Lesson 2 : -->
### 🟣 COURSE & CONTENT ENHANCEMENTS (New Models/Endpoints)
We need a more robust structure for lessons, including different content types and tracking progress.

1. **Content Model (e.g., Videos, Quizzes)**  **Done But `Permission not added`**
Lessons are just containers. Content is what's inside.

| Method	 |   Endpoint                    	   |   Description                           	    |  Permission                  |
| ---------- | ----------------------------------- | ---------------------------------------------- | ---------------------------- |
|  GET	     |   `/lms/lessons/<lesson_id>/content/` |	 List content within a lesson           	|  Enrolled student / Owner    |
|  GET       |   `/lms/lessons/<lesson_id>/content/`  |   List content within a specific lesson  |
|  GET       |   `/lms/courses/<course_id>/lessons/`  |   Show All lesson of specific course |  
|  GET       |   `/lms/course-data/<course_id>/`    |   Show all data of courses mean all lesson and all content | Enrolled Student / Owner | 


2.  **Progress Tracking & Completion:**
Track exactly where a student is in a course.

| Method  |  Endpoint                              | Description                                         | Permission    |
| ------- | ------------------------------------   |---------------------------------------------------- | ------------- |
| POST    |  /lms/progress/complete/<content_id>/  | Make a specific piece of content as completed       | Student Only  |  
| GET     |  /lms/progress/course/<course_id>/     | Get a student's full progress for a specific course | Student Only  |

3. **Quizzes & Assessments (New Features)**
A robust way to test knowledge 

| Method  |  Endpoint                    | Description                                         | Permission                |
| ------- | ---------------------------  | --------------------------------------------------- | ------------------------- |
| POST    |  /lms/quizzes/               | Make a specific piece of content as completed       | Instructor Only           |  
| GET     |  /lms/quizzes/<id>/          | Get a student's full progress for a specific course | Enrolled Student / Owner  |
| POST    |  /lms/quizzes/<id>/submit/   | Submit quiz answers                                 | Student Only              |

### 🟢 ENROLLMENT & STUDENT MANAGEMENT
Enhance how instructors manage their enrolled students and track their performance.

| Method   	| Endpoint	                             |    Description	                                        |  Permission               |
| --------- | -------------------------------------- | -------------------------------------------------------- | ------------------------- |
| GET   	| /lms/enrollments/my_courses/	         | List all courses the current user is enrolled in     	| Student Only              |
| GET   	| /lms/courses/<id>/analytics/	         | View course completion rates and average quiz scores	    | Instructor Only (Owner)   |
| POST   	| /lms/courses/<id>/grade/<student_id>/	 | Submit a grade for a student's completed course       	| Instructor Only (Owner)   |

## =========================================================================================================================================
## OPTIONAL :
### 🟡 PAYMENT & MONETIZATION (New Feature)
Allowing instructors to set prices for courses and accepting payment via integration (e.g., Stripe, PayPal).

| Method  |  Endpoint                              | Description                                         | Permission    |
| ------- | ------------------------------------   |---------------------------------------------------- | ------------- |
| POST    |  /lms/payment/create-checkout/         | Initiate a payment session for a specific course    | Student Only  |  
| POST    |  /lms/payment/webhook-listen/          | Receive payment confirmation (System Hook)          | Student Only  |
## =========================================================================================================================================


### ⚡ Summary of V2 Enhancements
By completing Version 2, your system will support:

✔ Detailed course content management (videos, text, etc.)
✔ Student progress tracking and completion markers
✔ Quizzes and automated grading
✔ Instructor dashboards for analytics
✔ Monetization and payment gateway integration
✔ A more professional and complete e-learning platform architecture

<!-- Version 3: -->
Version 3 adds robust community features like forums, notifications, profiles and verifiable certificates.

### 💬 FORUM/DISCUSSION ENDPOINTS
Manage Public Discussion within each course.


| Method     |	Endpoint	                     |  Description  |	Permission |
| ---------- |  -------------------------------  |  -----------  |	---------- |
| GET    	 |  /lms/forums/courses/<course_id>/ |  List all topics for a specific course  | Enrolled Only
| POST	     |  /lms/forums/topics/              |  Create a new discussion topic        | Enrolled Only
| GET	     |  /lms/forums/topics/`<id>`/	     |  Retrieve a single topic and its replies  | Enrolled Only
| PUT/DELETE |  /lms/forums/topics/`<id>`/	     |  Update or delete a topic               | Topic Owner
| POST	     |  /lms/forums/topics/`<id>`/reply/   |  Reply to an existing topic	           | Enrolled Only
| PUT/DELETE |  /lms/forums/replies/`<id>`/        |  Update or delete a specific reply      | Reply Owner

### 🔔 NOTIFICATION & MESSAGING ENDPOINTS
Provide users with real-time updates and internal messaging capabilities.

| Method	| Endpoint	| Description	| Permission |
| ------	| --------	| -----------	| ---------- |
| GET	    | /lms/notifications/	| Get all pending notifications for current user  |	Auth Only |
| POST	    | /lms/notifications/mark-read/	 | Mark all notifications as read	| Auth Only |
| POST	    | /lms/notifications/mark-read/<id>/	| Mark a single notification as read  |	Auth Only |
| (Socket)	| ws/lms/chat/<course_id>/	| WebSocket connection for live course group chat |	Enrolled Only |

### 👨‍🎓 USER PROFILES & DASHBOARD ENDPOINTS
Enhance user profile visibility and information management.

| Method |	Endpoint |	Description	| Permission  |
| ------ |	-------- |	----------	| ----------  |
| GET	| /lms/users/profile/<user_id>/	| View public user profile (bio, completed courses) |	Anyone |
| PUT/PATCH	| /lms/users/profile/me/	| Update current user's own bio and picture |	Auth Only |

### 📜 CERTIFICATES & VERIFICATION ENDPOINTS
Generate and verify course completion certificates.

| Method	| Endpoint	| Description	 | Permission |
| ---------	| --------	| -----------	 | ---------- |
| GET	| /lms/certificates/my-certificates/	| List all completed certificates for current user	 | Student Only |
| GET	| /lms/certificates/download/<id>/	| Download PDF certificate	 | Student Only |
| GET	| /lms/certificates/verify/<cert_id>/	| Public Endpoint to verify certificate  validity |	Anyone |


#### ⚡ Summary of V3 Features
✔ Real-time notifications system
✔ In-course live chat via WebSockets
✔ Integrated course discussion forums
✔ Public user profiles
✔ Verifiable certificates of completion


