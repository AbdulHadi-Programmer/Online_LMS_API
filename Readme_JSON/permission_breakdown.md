###  3 November 2025 : 

1. 🧠 The mental model (how DRF permission flow works)
2. ⚙️ Difference between has_permission() vs has_object_permission()
3. 🧩 When to use each (with examples)
4. 🧰 How to attach them to views correctly
5. 🧪 A step-by-step recipe to design your own permission


1. **The Mental Model —— What Permissions Really Are** 
Permissions are **gatekeepers.**
Every time a request hits a DRF view, DRF runs a security check pipeline before the view code executes.

DRF Flow looks like this :
```sql 
User sends request → Middleware → Authentication → Permission Check → Throttling → View Logic
```
So permissions run after authentication (i.e, request.user is already available)

2. **has_permisson() vs has_object_permission()**
Think of these as two different security levels.

`has_permission(self, request, view)`
- Runs before any object (model instance) is fetched.
- Used for view-level logic — e.g. “Only instructors can access POST /courses/”
- You don’t have access to any object yet here (because you haven’t fetched anything).

✅ Example:
```py
class IsInstructorOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: 
            return True 
        return bool(request.user and request.user.is_authenticated and request.user.is_instructor)        
```
Use it for : 
- Create, list, or global access control 
- Logic not tied to a specific model instance 


`has_object_permission(self, request, view, obj)`
- Runs after a specific object is fetched (like one course or lesson).
- Used for ownership-based rules —— e.g, "Only the instructor who owns this course can edit it."

Example :
```py
class IsCourseOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True 
        return obj.instructor == request.user 
```
Use it for : 
- Update / Delete / Retrieve object-level checks.
- Anything depending on a specific object field (`obj.owner`, `obj.course.instructor`, etc)

3. **When to Use Which :**

 | Scenario                                                     |  Methods to Use            | Why                                        |
| ------------------------------------------------------------- | -------------------------- | ------------------------------------------ |
| Only instructor can create new course                         | has_permission()           | Applies before object exists               |
| Only course owner can edit thier own course                   | has_object_permission()    | Depends on object ownership                | 
| Anyone can view courses, but only instructors can delete them | both                       |  Read = SAFE_METHODS;  DELETE = restricted | 
| Students can only review courses they're enrolled in          | has_object_permision()     | Tied to specific course/student            |
|

4. **How to Attach Permission to Views:**
**1️⃣ Class-level permissions:**
Most Comman and Cleanest.

```py
from rest_framework.permissions import IsAuthenticated 
from .permissions import IsInstructorOnly, IsCourseOwnerOrReadOnly

class CourseAPIView(APIView):
    permission_classes = [IsAuthenticated, IsInstructorOnly]

    def get(self, request):
        ...
```
DRF automatically runs all `has_permission()` methods in your `permission_classes` list before entering the view.

2. **Object-level Permissions**
In APIView, you must explicitly call :
```py
self.check_object_permissions(request, obj)
```
because DRF does not automatically run object-level checks (unlike ModelViewSet, which does).

Example: 
```py
class CourseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCourseOwnerOrReadOnly]

    def get_object(self, pk):
        course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(self.request, course)
        return course 
    
    def get(self, request, pk):
        course = self.get_object(pk)

```
Now your `IsCourseOwnerOrReadOnly.has_object_permission()` automatically runs inside `check_object_permissions()`.


### 🧩 Step 1: Identify what your permission protects.
Is it view-level (“who can create or list?”) or object-level (“who can edit this specific one?”)?

### 🧩 Step 2: Start from the base class
```py 
from rest_framework.permissions import BasePermission, SAFE_METHODS 
```

### 🧩 Step 3: Choose the right method
- Use `has_permission()` if the logic applies before fetching data
- Use `has_object_permission()` if it’s about ownership or one instance

### 🧩 Step 4: Add authentication guard
Always include:
```py
if not request.user or not request.user.is_authenticated:
    return False 
```

### 🧩 Step 5: Define logic clearly
Examples:
```py
# Example A — Instructor-only creation
class IsInstructorOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_instructor
```
```py
# Example B — Course owner can update
class IsCourseOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.instructor == request.user
```
```py
# Example C — Student enrolled check 
class IsEnrolledStudent(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Enrollment.object.filter(course=obj, student= request.user)
```

### Bonus Tip: Combining Permissions
If you assign multiple permissions like this :
```py
permission_classes = [IsAuthenticated, IsInstructorOnly]
```
DRF runs them in AND logic:
- All permissions must return `True` for access to be granted.
If you want "Instructor OR Admin", you write a custom permission handling both inside one class.


#### Summary: 
| Concept                           | Purpose                                   | Typical Use            |
| --------------------------------- | ----------------------------------------- | ---------------------- |
| `has_permission()`                | Global access control                     | Create/List routes     |
| `has_object_permission()`         | Object-specific control                   | Retrieve/Update/Delete |
| `self.check_object_permissions()` | Manually triggers object permission check | Required in `APIView`  |
| `permission_classes = [...]`      | Registers permissions for a view          | Class-level control    |


