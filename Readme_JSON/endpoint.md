### LMS 2nd Version :

1. **Student Only Endpoints (Which run with Student token)**
ye sab student ke personal actions ya data ke liye hain.

| Endpoint | Kaam |Expected Behavior (Student Token) |
| -------- | ---- | -------------------------------- |
| `/enrollments/my-courses/` | Apne enrolled courses list|200 OK + list |
| `/progress/complete/<content_id>/` | Content mark as complete | 200/201 |
| `/progress/course/<course_id>/` | Apna progress percentage | 200 OK + % |
| `/course-data/<course_id>/` | Pura course (lessons + content) nested data | 200 OK (agar enrolled hai) |
| `/reviews/` (POST) | Course review dena | 201 (agar enrolled hai) |

Agar student token se yeh chal raha hain -> perfect! 


2. **Instructor Only Endpoints (Instructor token se chalenga )**
Yeh Instructor ka management aur analytics ke liye: 

| Endpoint | kaam | Expected Behaviour (Instructor token)         |
| -------- | ---- | --------------------------------------------- |
| `/courses/` **(POST)** |  Naya course banana  | 201 |
| `/courses/<pk>` **(PUT/PATCH/DELETE)** | Apna course edit/delete  | 200/204 |
| `/lessons/` **(POST)** | lesson banana  | 201 |
| `/lessons/<pk>` **(PUT/PATCH/DELETE)** | Apna Lesson edit/delete  | 200/204 |
| `/content/` **(POST)** |  Content Banana | 201 |
| `/content/<id>` **(PUT/PATCH/DELETE)** |  Content edit/delete | 200/204 |
| `/lessons/<lesson_id>/content/`  | Specific lesson mein content  |  201  | 
| `/instructor-course/` | Apne saare courses list  |  200 OK  | 
| `/courses/<id>/analytics` | Apne course ka analytics  | 200 OK + stats  | 
| `/courses/<id>/grade/<student_id>` **(POST)** | Student ko grade dena  | 201 | 
Yeh sab sirf instructor token se chalenga -- student token se 403 Forbidden aayega (jo sahi hai!)


3. **Comman / Mixed Endpoints (Dono ya Public)**
| Endpoint | kaam | Kaam  | Student Token | Instructor token |
| -------- | ---- | ----- | ------------- | ---------------- |
| `/courses/` (GET) | Sab courses list  | 200 | 200 |
| `/courses/<pk>/` (GET) | Course detail  | 200 | 200 |

| `/lessons/` (GET) | Sab lessons  | 200 | 200 |
| `/lessons/<pk>` (GET) | Lesson detail  | 200 | 200 |

| `/categories/` | Category list | 200 | 200 |
| `/categories/<id>` | Specific Category | 200 | 200 |

| `/reviews/` (GET) | Sab reviews | 200 | 200 |
| `/reviews/<pk>` (GET) | Specific reviews | 200 | 200 |

| `/content/` (GET) | Sab Content | 200 | 200 |
| `/content/<id>` (GET) | Specific Content | 200 | 200 |

| `/lessons/<lesson_id>/content/` (GET) | Lesson ka content | 200 | 200 |
| `/courses/<course_id>/lessons/` (GET) | Course ke lessons | 200 | 200 |



