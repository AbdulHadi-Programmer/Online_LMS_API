### Logical Permission Scenarios :
Here are realistic, custom permission ideas for your LMS: 
 | Model     |  Who can do what                                             | Permission Idea              |
| ---------- | ------------------------------------------------------------ | ---------------------------- |
| Course     | Only the Intructor who created it can update/delete          | IsCourseInstructorOrReadOnly |
| Lesson     | Only the Course's Intrucrtor can create/update/delete lesson | IsLessonInstructorOrReadOnly |
| Enrollment | Only Students can enroll; instructor/admin can view          | IsStudentOnly                |
| Review     | Only students enrolled in a course can leave a review        | IsEnrolledStudentForReview   |
| Category   | Only admin/superuser can create / update / delete            | IsAdminOrReadOnly            |
|            |                                                              |                              | 


