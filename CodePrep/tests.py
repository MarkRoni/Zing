from django.test import TestCase
from CodePrep.models import Course, UserProfile, Review, Subject, Provider, LearningStyle, save_rating
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

import sys
sys.path.append('E:/ITECH/CodePrep/')
import populate_codeprep

class CourseTests(TestCase):
    def setUp(self):
        courses = {
            "Python for Everybody":
                {"subject" : "testsubject",
                "overview" : "This Specialization builds on the success of the Python for Everybody course and will introduce fundamental programming concepts including data structures, networked application program interfaces, and databases, using the Python programming language. In the Capstone Project, you’ll use the technologies learned throughout the Specialization to design and create your own applications for data retrieval, processing, and visualization.",
                "provider" : "testprovider",
                "style" : ["teststyle"],
                "courselink" : "https://www.coursera.org/specializations/python",
                "price" : 400,
                "rating" : 1},
            "Java Programming and Software Engineering Fundamentals":
                {"subject" : "testsubject",
                "overview" : "Take your first step towards a career in software development with this introduction to Java—one of the most in-demand programming languages and the foundation of the Android operating system. Designed for beginners, this Specialization will teach you core programming concepts and equip you to write programs to solve complex problems. In addition, you will gain the foundational skills a software engineer needs to solve real-world problems, from designing algorithms to testing and debugging your programs.",
                "provider" : "testprovider",
                "style" : ["teststyle"],
                "courselink" : "https://www.coursera.org/specializations/java-programming",
                "price" : 400,
                "rating" : 2}}

        subjects = {"testsubject"}

        providers = {
            "testprovider" : {"logolink" : "/static/images/provider_logos/Coursera.png"}}

        learningstyles = {"teststyle"}

        for subject in subjects:
            print("Adding subject: "+subject)
            s = populate_codeprep.add_subject(subject)

        for provider, provider_data in providers.items():
            print("Adding Provider: "+provider+" With logo link: ..."+provider_data["logolink"][-25:])
            p = populate_codeprep.add_provider(provider, provider_data["logolink"])

        for learningstyle in learningstyles:
            print("Adding leaning style: "+learningstyle)
            l = populate_codeprep.add_style(learningstyle)

        for course, course_data in courses.items():
            c = populate_codeprep.add_course(course, course_data["subject"], course_data["overview"],
                course_data["provider"], course_data["style"],course_data["courselink"],
                course_data["price"], course_data["rating"])

# Unfortunately this test now fails, as I had to remove the validators. They were
# causing problems when bringing in data, and I couldn't find a fix in time.
    def test_ensure_rating_between_0_and_5(self):
        course = Course.objects.get(name="Python for Everybody")
        course.rating = -1
        try:
            course.full_clean()
        except ValidationError:
            print("Test passed, rating value of -1 not allowed")
        else:
            course.save()
            print("Test failed, rating value of -1 allowed")

    def test_slug_creation(self):
        course = Course.objects.get(name="Python for Everybody")
        self.assertEqual(course.slug, 'python-for-everybody')

    def test_ensure_rating_calculated(self):
        course = Course.objects.get(name="Java Programming and Software Engineering Fundamentals")
        review1 = Review.objects.get_or_create(
            course=course,rating=4,
            user=User.objects.get_or_create(username="testuser1",password="passwordsuck")[0])
        review2 = Review.objects.get_or_create(
            course=course,rating=2,
            user=User.objects.get_or_create(username="testuser2",password="theyreallydo")[0])
        course.rating = save_rating(course)
        course.save()
        self.assertEqual(course.rating, 3)

class UserTests(TestCase):
    def test_ensure_user_has_password(self):
        user = User(username="testuser")
        try:
            user.full_clean()
        except Exception as e:
            print("Error: "+str(e))
            print("Test passed, user without password not alllowed")
        else:
            user.save()
            print("Test failed, user without password allowed")

    def test_ensure_userprofile_has_user(self):
        userprofile = UserProfile()
        try:
            userprofile.full_clean()
        except Exception as e:
            print("Error: "+str(e))
            print("Test passed, user profile without user not alllowed")
        else:
            user.save()
            print("Test failed, user profile without user allowed")


class SearchViewTests(TestCase):
    def test_search_page_displays_form(self):
        response = self.client.get(reverse('search_course'))
        self.assertContains(response, 'form')
