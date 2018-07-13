from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg


# Model representing online course providers. Foreign Key for Course
class Provider(models.Model):
    name = models.CharField(max_length=128, unique=True)
    logolink = models.URLField()

    def __str__(self):
        return self.name

# A courses only cover one topic - perhaps this can be an attribute
# of a course rather than a whole model - Marcus
# Model representing the subject of a course
class Subject(models.Model):
    subject = models.CharField(max_length=128)

# Model representing the various learning styles in which courses are offered
# Used to categorize and filter courses
class LearningStyle(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

# Model representing the courses whose details are stored on the site
class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=0)
    overview = models.TextField(max_length=1000)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, default=0)
    style = models.ManyToManyField(LearningStyle)
    courselink = models.URLField()
    price = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    rating = models.IntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.rating = save_rating(self)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Model which stores the custom data related to Users
# Contains field linking it to an AuthUser
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    enrolledcourses = models.ManyToManyField(Course)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

# Model representing user reviews of courses
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=True)
    comment = models.TextField(max_length=5000)

    def __str__(self):
        return self.id

# Function for updating course average rating
def save_rating(course):
    # Check for existing reviews for this course
    try:
        coursereviews = Review.objects.filter(course=course)
        courserating = coursereviews.aggregate(avg=Avg('rating'))['avg']
    # If no reviews found, average course rating is 0
    except Review.DoesNotExist:
        courserating = 0
    return courserating
