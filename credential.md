## 2 December (Access token valid today and 9 December refresh token valid)
```json
// Credential Of Admin (Valid till Refresh: 1Month, Access: 7 Days)
{

}
```

1. Users (CustomUser):
```json
[
    {"username": "sara", "password": "123", "is_instructor": true},

    {"username": "mark", "password": "123", "is_instructor": true}, 
    
    {"username": "alice", "password": "123", "is_instructor": true}, 
    
    {"username": "bob", "password": "123", "is_student": true}, 
    
    {"username": "charlie", "password": "123", "is_student": true}, 
]
```
2. Categories:
```json 
[
    {"name":"Mobile Apps", "description": "Android and IOS development"}
]
```

3. Courses: 
```json
[
    {"title": "React from Zero to Hero", "description": "Frontend UI with React.js", "price": "1200.00", "category": 1, "instructor": 2},
]
```
5. Enrollments:
```json
[
    {"student": 4, "course": 1, "progress":50.0},
    {"student": 5, "course": 1, "progress":80.0},
    {"student": 4, "course": 3, "progress":30.0},
    {"student": 6, "course": 2, "progress":60.0},
    {"student": 5, "course": 2, "progress":10.0},
] 
```
> ⚠️ Remember: For enrollment API, you must be logged in as the student, because your view usually does serializer.save(user=request.user). Admin cannot POST via API unless you remove that restriction.

6. Reviews: 
```json
[
    {"student":4, "course": 1, "rating":5, "comment": "Excellent course!"}, 
    {"student":5, "course": 1, "rating":4, "comment": "Very good, but could use more example."}, 
    {"student":6, "course": 2, "rating":5, "comment": "Prefer into to react"}, 
    {"student":4, "course": 3, "rating":3, "comment": "Good start but too short "}, 
] 
```
> Same rule: To POST via API, user must be enrolled in that course and logged in. Admin can still add reviews manually in admin or api.

