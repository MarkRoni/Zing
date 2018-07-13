import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'CodePrepProject.settings')

import django
django.setup()
from CodePrep.models import Provider, Course, Subject, LearningStyle, Review
from django.contrib.auth.models import User
from django.db.models import Avg

def populate():
    courses = {
        "Python for Everybody":
            {"subject" : "Python",
            "overview" : "This Specialization builds on the success of the Python for Everybody course and will introduce fundamental programming concepts including data structures, networked application program interfaces, and databases, using the Python programming language. In the Capstone Project, you’ll use the technologies learned throughout the Specialization to design and create your own applications for data retrieval, processing, and visualization.",
            "provider" : "Coursera",
            "style" : ["Scheduled","Certified"],
            "courselink" : "https://www.coursera.org/specializations/python",
            "price" : 400,
            "rating" : 1},
        "Java Programming and Software Engineering Fundamentals":
            {"subject" : "Java",
            "overview" : "Take your first step towards a career in software development with this introduction to Java—one of the most in-demand programming languages and the foundation of the Android operating system. Designed for beginners, this Specialization will teach you core programming concepts and equip you to write programs to solve complex problems. In addition, you will gain the foundational skills a software engineer needs to solve real-world problems, from designing algorithms to testing and debugging your programs.",
            "provider" : "Coursera",
            "style" : ["Scheduled","Certified"],
            "courselink" : "https://www.coursera.org/specializations/java-programming",
            "price" : 400,
            "rating" : 2},
        "Introduction to Python":
            {"subject" : "Python",
            "overview" : "Get started writing Python with this introductory course.",
            "provider" : "Udacity",
            "style" : ["Self-paced", "Video-based", "Interactive"],
            "courselink" : "https://eu.udacity.com/course/introduction-to-python--ud1110",
            "price" : 0,
            "rating" : 3},
        "Android Basics by Google" :
            {"subject" : "Java",
            "overview" : "Want to develop Android apps, but don’t know where to start? In this Nanodegree program, we’ll show you the way. We developed this curriculum with Google for true beginners interested in developing apps for the next billion Android users!",
            "provider" : "Udacity",
            "style" : ["Video-based", "Certified", "Scheduled", "Projects"],
            "courselink" : "https://eu.udacity.com/course/android-basics-nanodegree-by-google--nd803",
            "price" : 200,
            "rating" : 4},
        "Intro to JavaScript" :
            {"subject" : "JavaScript",
            "overview" : "JavaScript is the most popular programming language for both front-end and back-end web development. Applications for JavaScript span from interactive websites to the Internet of Things, making it a great choice for beginners and experienced developers looking to learn a new programming language.",
            "provider" : "Udacity",
            "style" : ["Self-paced", "Video-based", "Interactive", "Projects"],
            "courselink" : "https://eu.udacity.com/course/intro-to-javascript--ud803",
            "price" : 0,
            "rating" : 5},
        "Intro to HTML and CSS" :
            {"subject" : "HTML & CSS",
            "overview" : "In this course you will learn how to convert digital design mockups into static web pages. We will teach you how to approach page layout, how to break down a design mockup into page elements, and how to implement that in HTML and CSS. You will also learn about responsive design techniques, which are increasingly important in a world where mobile devices and TV screens are used more and more often to look for information and entertainment.",
            "provider" : "Udacity",
            "style" : ["Self-paced", "Video-based", "Interactive"],
            "courselink" : "https://eu.udacity.com/course/intro-to-html-and-css--ud304",
            "price" : 0,
            "rating" : 2},
        "Front End Development Certification: HTML5 and CSS" :
            {"subject" : "HTML & CSS",
            "overview" : "The first section will teach you the basics of how webpages work and also introduce you to JavaScript programming. Skills you'll practice include HTML, CSS, JavaScript, jQuery and Bootstrap. To earn this certification, you'll build 10 front-end projects and implement many JavaScript algorithms.",
            "provider" : "freeCodeCamp",
            "style" : ["Interactive", "Self-paced", "Projects", "Certified"],
            "courselink" : "https://www.freecodecamp.org/",
            "price" : 0,
            "rating" : 3},
        "Front End Development Certification: JavaScript" :
            {"subject" : "JavaScript",
            "overview" : "The first section will teach you the basics of how webpages work and also introduce you to JavaScript programming. Skills you'll practice include HTML, CSS, JavaScript, jQuery and Bootstrap. To earn this certification, you'll build 10 front-end projects and implement many JavaScript algorithms.",
            "provider" : "freeCodeCamp",
            "style" : ["Interactive", "Self-paced", "Projects", "Certified"],
            "courselink" : "https://www.freecodecamp.org/",
            "price" : 0,
            "rating" : 4},
        "Python 3 Tutorial" :
            {"subject" : "Python",
            "overview" : "Learn Python, one of today's most in-demand programming languages on-the-go, while playing, for FREE! Compete and collaborate with your fellow SoloLearners, while surfing through short lessons and fun quizzes. Practice writing Python code within the app, collect points, and show off your skills.",
            "provider" : "SoloLearn",
            "style" : ["Self-paced", "Interactive"],
            "courselink" : "https://www.sololearn.com/Course/Python/",
            "price" : 0,
            "rating" : 3},
        "Java Tutorial" :
            {"subject" : "Java",
            "overview" : "SoloLearn's Learn Java is a comprehensive guide to one of the most popular programming languages in the world. And here's a big bonus: Learn Java is FREE! The Learn Java lessons are fast, easy, and effective; the app is set up so that you can complete the work in less than three hours. No prior programming experience is needed.",
            "provider" : "SoloLearn",
            "style" : ["Self-paced", "Interactive"],
            "courselink" : "https://www.sololearn.com/Course/Java/",
            "price" : 0,
            "rating" : 1},
        "JavaScript Tutorial" :
            {"subject" : "JavaScript",
            "overview" : "Learn all of the fundamentals of JavaScript, and have fun while doing it – with SoloLearn! This tutorial covers all basic features of JavaScript programming, including ways to make your website more interactive, create change website content, validate forms, create cookies, and so much more. Go through our carefully selected instructional lessons, then take interactive quizzes while exploring checkpoints.",
            "provider" : "SoloLearn",
            "style" : ["Self-paced", "Interactive"],
            "courselink" : "https://www.sololearn.com/Course/JavaScript/",
            "price" : 0,
            "rating" : 5},
        "Learning Python" :
            {"subject" : "Python",
            "overview" : "Python—the popular and highly readable object-oriented language—is both powerful and relatively easy to learn. Whether you're new to programming or an experienced developer, this course can help you get started with Python. Joe Marini provides an overview of the installation process, basic Python syntax, and an example of how to construct and run a simple Python program. Learn to work with dates and times, read and write files, and retrieve and parse HTML, JSON, and XML data from the web.",
            "provider" : "Lynda",
            "style" : ["Self-paced", "Video-based", "Certified"],
            "courselink" : "https://www.lynda.com/Python-tutorials/Learning-Python/661773-2.html",
            "price" : 30,
            "rating" : 3},
        "Learning Java" :
            {"subject" : "Java",
            "overview" : "Java is one of the top-five programming languages, and is used for websites, embedded controllers, and Android app development. This is an introduction to get you started programming with Java. Peggy Fisher introduces the basics: data types, strings, arrays, expressions, loops, and functions. She'll help you control the flow and logic of your code, and create classes using the principles of object-oriented design. Then go a bit beyond the basics and learn advanced techniques for working with arrays, manipulating files, and building graphical user interfaces (GUIs) that respond to user input. This three-hour capsule course is perfect for developers who need to get up to speed with Java fast, as well as for beginning programmers who want their first taste of this popular language.",
            "provider" : "Lynda",
            "style" : ["Self-paced", "Video-based", "Certified"],
            "courselink" : "https://www.lynda.com/Java-tutorials/Up-Running-Java/184457-2.html",
            "price" : 30,
            "rating" : 2},
        "Learning ECMAScript 6" :
            {"subject" : "JavaScript",
            "overview" : "Meet the future of JavaScript: ECMAScript 6. This short course takes a look at the latest features of ECMAScript 6 (aka ES6) and how these changes are making JavaScript even more powerful and concise. Eve Porcello reviews the new keywords and function/object syntax and shows how the new class syntax can be used with React, the popular JavaScript library. You'll also review the ES6 compiling tool Babel, and use Babel to make your ES6 code compatible with modern browsers.",
            "provider" : "Lynda",
            "style" : ["Self-paced", "Video-based", "Certified"],
            "courselink" : "https://www.lynda.com/JavaScript-tutorials/Learning-ECMAScript-6/424003-2.html",
            "price" : 30,
            "rating" : 4},
        "Learn Python" :
            {"subject" : "Python",
            "overview" : "This course is a great introduction to both fundamental programming concepts and the Python programming language. By the end, you'll be familiar with Python syntax and you'll be able to put into practice what you'll have learned in a final project you'll develop locally.",
            "provider" : "Codeacademy",
            "style" : ["Interactive", "Self-paced"],
            "courselink" : "https://www.codecademy.com/learn/learn-python",
            "price" : 0,
            "rating" : 3},
        "Learn Java" :
            {"subject" : "Java",
            "overview" : "In this course you'll be exposed to fundamental programming concepts, including object-oriented programming (OOP) using Java. You'll build 7 Java projects—like a basic calculator—to help you practice along the way.",
            "provider" : "Codeacademy",
            "style" : ["Interactive","Self-paced"],
            "courselink" : "https://www.codecademy.com/learn/learn-java",
            "price" : 0,
            "rating" : 3},
        "Introduction to JavaScript" :
            {"subject" : "JavaScript",
            "overview" : "You will learn introductory level object oriented programming using ES6 JavaScript. This course sequence covers data types and structures, functions, and object-oriented programming with classical inheritance. Though you will learn these concepts in the context of ES6 syntax, are required knowledge for understanding object oriented programming.",
            "provider" : "Codeacademy",
            "style" : ["Interactive","Self-paced"],
            "courselink" : "https://www.codecademy.com/learn/introduction-to-javascript",
            "price" : 0,
            "rating" : 4},
        "Build Websites from Scratch" :
            {"subject" : "HTML & CSS",
            "overview" : "This program goes beyond definitions and into the best practices of expert developers. You'll ease in with the basics and quickly ramp up to confidently build websites with pixel-perfect accuracy.",
            "provider" : "Codeacademy",
            "style" : ["Projects", "Scheduled", "Projects", "Certified"],
            "courselink" : "https://www.codecademy.com/pro/intensive/build-websites-from-scratch",
            "price" : 199,
            "rating" : 5},
        }

    subjects = {"Python", "Java", "JavaScript", "HTML & CSS"}

    providers = {
        "Coursera" : {"logolink" : "/static/images/provider_logos/Coursera.png"},
        "Udemy" : {"logolink" : "/static/images/provider_logos/Udemy.png"},
        "Udacity" : {"logolink" : "/static/images/provider_logos/Udacity.png"},
        "SoloLearn" : {"logolink" : "/static/images/provider_logos/sololearn.jpg"},
        "Lynda" : {"logolink" : "/static/images/provider_logos/lynda.jpg"},
        "Codeacademy" : {"logolink" : "/static/images/provider_logos/Codecademy.png"},
        "TreeHouse" : {"logolink" : "/static/images/provider_logos/Treehouse.png"},
        "freeCodeCamp" : {"logolink" : "/static/images/provider_logos/freeCodeCamp.jpg"}}

    learningstyles = {"Scheduled", "Self-paced", "Projects", "Video-based", "Interactive", "Certified"}

    users = {"John" : {"email" : "johnperkings@gmail.com"},
            "Maria" : {"email" : "mariajohnstone@gmail.com"},
            "Andrew" : {"email" : "andrewsmith@gmail.com"},
            "Caroline" : {"email" : "caroliness@gmail.com"}}

    reviews = {
        "001" :
            {"user" : "John",
             "course" : "Python for Everybody",
             "rating" : 4,
             "comment" : "it was great, I learned so much and it was easy to follow."},
        "002" :
            {"user" : "John",
             "course" : "Java Programming and Software Engineering Fundamentals",
             "rating" : 3,
             "comment" : "Java is confusing for me, but this course did help me come to terms with OOP."},
        "003" :
            {"user" : "Maria",
             "course" : "Introduction to Python",
             "rating" : 4,
             "comment" : "Python is great! I loved learning about such an intuitive language."},
        "004" :
            {"user" : "Maria",
             "course" : "Android Basics by Google",
             "rating" : 5,
             "comment" : "All the material was interesting and now I have a better understanding of my favourite devices. Great stuff."},
        "005" :
            {"user" : "Andrew",
             "course" : "Intro to JavaScript",
             "rating" : 2,
             "comment" : "I was a little confused by JavaScript, enough to make the course hard to follow. But I'm sure it's very useful."},
        "006" :
            {"user" : "Andrew",
             "course" : "Intro to HTML and CSS",
             "rating" : 3,
             "comment" : "The instructor made getting to grips with HTML easy. I especially liked the interactive exercises."},
        "007" :
            {"user" : "Andrew",
             "course" : "Front End Development Certification: HTML5 and CSS",
             "rating" : 4,
             "comment" : "Extremely challenging course, but very rewarding. Highly recommend to anyone who wants to get certified."},
        "008" :
            {"user" : "Caroline",
             "course" : "Front End Development Certification: JavaScript",
             "rating" : 4,
             "comment" : "Amazing course, learned about just how complex websites can be."},
        "009" :
            {"user" : "Caroline",
             "course" : "Python 3 Tutorial",
             "rating" : 2,
             "comment" : "I don't think Python is for me, but maybe it was just the strange method of teaching which the instructor insisted on."},
        "010" :
            {"user" : "Caroline",
             "course" : "Java Tutorial",
             "rating" : 3,
             "comment" : "Java seems really interesting, the only downside to this course was maybe the small amount of material covered."},
        "011" :
            {"user" : "John",
             "course" : "JavaScript Tutorial",
             "rating" : 3,
             "comment" : "Maybe it's me but this course was quite challenging for beginner-level. It got me interested in learning more though."},
        "012" :
            {"user" : "John",
             "course" : "Learning Python",
             "rating" : 5,
             "comment" : "Python seems to make much more sense than Javascript to me, and the instructor of this course was excellent."},
        "013" :
            {"user" : "Andrew",
             "course" : "Learning Java",
             "rating" : 1,
             "comment" : "Java seems boring, I'm not sure why I chose to take this course, let alone finish it. Would not recommend."},
        "014" :
            {"user" : "Andrew",
             "course" : "Learning ECMAScript 6",
             "rating" : 3,
             "comment" : "This course might have been too high-level for me, but I stuck with it and it was rewarding."},
        "015" :
            {"user" : "Maria",
             "course" : "Learn Python",
             "rating" : 4,
             "comment" : "Python is awesome, I never got any strange unexplained errors in any of the exercises. Might take it again as a refresher in the future."},
        "016" :
            {"user" : "Maria",
             "course" : "Learn Java",
             "rating" : 2,
             "comment" : "This course was ok, the instructor was good but the exercises weren't very helpful, I didn't feel like I learned a lot."},
        "017" :
            {"user" : "John",
             "course" : "Introduction to JavaScript",
             "rating" : 4,
             "comment" : "JavaScript, or JS as I like to call it, is really cool and I can't wait to try out all the stuff I learned in this course."},
        "018" :
            {"user" : "Caroline",
             "course" : "Build Websites from Scratch",
             "rating" : 5,
             "comment" : "It's amazing how easy it is to make your own website, instead of using one of those services. This course taught me so much great stuff."},
        "019" :
            {"user" : "Maria",
             "course" : "Build Websites from Scratch",
             "rating" : 4,
             "comment" : "I thoroughly enjoyed this course, I can't wait to try making my own blog where I can write about all the stories behind my instagram photos."},
             }

    for subject in subjects:
        print("Adding subject: "+subject)
        s = add_subject(subject)

    for provider, provider_data in providers.items():
        print("Adding Provider: "+provider+" With logo link: ..."+provider_data["logolink"][-25:])
        p = add_provider(provider, provider_data["logolink"])

    for learningstyle in learningstyles:
        print("Adding leaning style: "+learningstyle)
        l = add_style(learningstyle)

    for user, user_data in users.items():
        print("Adding user: "+user)
        u = add_user(user, user_data["email"])

    for course, course_data in courses.items():
        print("Adding data on course "+course)
        print("\tSubject: "+course_data["subject"])
        print("\tOverview: "+course_data["overview"][:72]+"...")
        print("\tProvider: "+course_data["provider"])
        print("\tLink: "+course_data["courselink"])
        print("\tPrice: "+str(course_data["price"]))
        print("\tLearning Styles: "+ ", ".join(course_data["style"]))
        print("\tAverage Rating: "+str(course_data["rating"]))
        c = add_course(course, course_data["subject"], course_data["overview"],
            course_data["provider"], course_data["style"],course_data["courselink"],
            course_data["price"], course_data["rating"])

    for review, review_data in reviews.items():
        print("Adding review " + str(review))
        r = add_review(review, review_data["user"], review_data["course"],
         review_data["rating"], review_data["comment"])

def add_course(name, subject, overview, provider, style, courselink, price, rating):
    c = Course.objects.get_or_create(name=name)[0]
    c.subject = Subject.objects.get(subject=subject)
    c.overview = overview
    c.provider = Provider.objects.get(name=provider)
    c.courselink = courselink
    c.price = price
    c.rating = rating
    c.save()
    for s in style:
        link = LearningStyle.objects.filter(name=s).get()
        c.style.add(link)
    return c

def add_subject(subject):
    s = Subject.objects.get_or_create(subject=subject)[0]
    s.save()
    return s

def add_provider(name, logolink):
    p = Provider.objects.get_or_create(name=name)[0]
    p.logolink = logolink
    p.save()
    return p

def add_style(name):
    l = LearningStyle.objects.get_or_create(name=name)[0]
    l.save()
    return l

def add_user(name, email):
    u = User.objects.get_or_create(username=name)[0]
    u.email = email
    u.save()
    return u

def add_review(review, user, course, rating, comment):
    r = Review.objects.get_or_create(user = User.objects.get(username=user), course = Course.objects.get(name=course))[0]
    r.rating = rating
    r.comment = comment
    r.save()
    return r

# Start execution here
if __name__ == '__main__':
    print("Starting CodePrep population script...")
    populate()
