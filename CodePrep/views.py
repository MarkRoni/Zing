from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from CodePrep.models import UserProfile, User, Course, Provider, Subject, LearningStyle, Review, save_rating
from CodePrep.forms import UserProfileForm, ReviewForm, SearchForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from social_django.models import UserSocialAuth
from django.views.decorators.csrf import csrf_exempt


# Index page view
def index(request):
    # Get all relevant data that will be used somewhere on index page
    courses_list = Course.objects.all()
    providers_list = Provider.objects.all()
    reviews_list = Review.objects.all()
    context_dict = {'courses' : courses_list,'providers' : providers_list,
        'reviews' : reviews_list}
    response = render(request, 'codeprep/index.html', context_dict)
    return response

# About page view
def about(request):
    response = render(request, 'codeprep/about.html', {})
    return response

# Profile registration view (registration 2nd step)
@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form':form}

    return render(request, 'codeprep/profile_registration.html', context_dict)

# User Profile view
@login_required
def profile(request, username):
    # Check for valid user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    # Load user profile data
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture})

    enrolledcourses = userprofile.enrolledcourses.all()

    # Allow updating of user profile from profile page
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            # return user to their profile page upon successful update
            return redirect('profile', user.username)
        else:
            print(form.errors)

    context_dict = {'userprofile': userprofile, 'selecteduser': user,
        'form': form, 'enrolledcourses' : enrolledcourses}
    return render(request, 'codeprep/profile.html', context_dict)

# Disable Profile
@login_required
def disable_profile(request):
    user = request.user
    user.is_active = False
    user.email = ""
    UserSocialAuth.objects.filter(user=request.user).delete()
    user.save()
    messages.success(request, 'Profile successfully disabled.')
    return redirect('auth_logout')

# Course Details view
def show_course(request, course_name_slug):
    context_dict = {}

    # Check for valid course
    try:
        course = Course.objects.get(slug=course_name_slug)
        context_dict['course'] = course
    except Course.DoesNotExist:
        context_dict['course'] = None

    # Load course learning styles
    styles = course.style.all()
    context_dict['styles'] = styles

    # Load course reviews and update average rating
    context_dict['reviews'] = get_coursereviews(course)
    course.rating = save_rating(course)
    course.save()

    return render(request, 'codeprep/course.html', context_dict)

# Review Course view
@login_required
def review_course(request, course_name_slug):
    context_dict = {}
    current_user = request.user

    # Check for valid course
    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        course = None

    form = ReviewForm()

    # Store new review if form has been filled
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if course:
                review = form.save(commit=False)
                review.user = current_user # reviewer is currently logged in user
                review.course = course # course is course page who sent us here
                review.save()
                # return user to course page if review submission is successful
                return show_course(request, course.slug)
            else:
                print(form.errors)

    else:
        context_dict = {'form' : form, 'course' : course, 'user' : current_user}
        return render(request, 'codeprep/reviewcourse.html', context_dict)

# Social Login Settings view
@login_required
def settings(request):
    user = request.user
    # Check for linked github account
    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    # Check for linked twitter acount
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    # Check for linked facebook account
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None
    # User can disconnect their social login only if they've set a password
    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'registration/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

# Password Change view
@login_required
def password(request):
    # Check for usable password
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed successfully.')
            return redirect('password')
        else:
            messages.error(request, 'Incorrect details provided.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})

# Course Search view
def search_courses(request):
    form = SearchForm
    context_dict = {"form":form}
    return render(request, 'codeprep/search.html', context_dict)

# Search Results view
def search_results(request):
    # Get search parameters from request
    search = request.GET.get('subject')
    filters = request.GET.getlist('style') # Construct a list of learning style IDs
    price = request.GET.get('price')
    order = request.GET.get('order')
    # Print parameters for testing
    print("order mode = "+str(order))
    print("Search term = "+search)
    print(request.GET.getlist("style"))
    print(request.GET.get('price'))
    if request.method == 'GET':
        # Construct query based on 'order' and 'search' and store result
        if order != None:
            print("ordering results")
            data = list(c for c in Course.objects.order_by(order).prefetch_related('subject').all() if (search.lower() in c.subject.subject.lower()))
        else:
            data = list(c for c in Course.objects.prefetch_related('subject').all() if (search.lower() in c.subject.subject.lower()))
        if filters != []: # if there are learning styles to filter by...
            for filter_id in filters:
                 # filter the current list of courses by those that contain each filter id
                data = [course for course in data if course.style.filter(id=filter_id)]
        # If 'only free courses' selected, filter for price = 0
        if price == 'on':
            data = [course for course in data if (course.price == 0)]
        # Make sure course average rating is up-to-date
        for d in data:
            d.rating = save_rating(d)

    # Print results for testing
    for d in data:
        print(d.name)

    return render(request, 'codeprep/search_results.html', {"courses":data, "form":SearchForm})

@csrf_exempt
def suggest(request):
    # Get incomplete search term
    search = request.POST['search']

    # Search for pattern from list
    suggestion = ""
    suggestion_list = ["Java", "Python", "HTML & CSS", "JavaScript"]
    #list(Subject.objects.all().values('subject')
    for s in suggestion_list:
        if s.startswith(search):
            suggestion = s

    # Return suggestion
    response = HttpResponse(suggestion)
    return response

# Function for gettings reviews for a certain course
def get_coursereviews(course):
    try:
        coursereviews = Review.objects.filter(course=course)
    except Review.DoesNotExist:
        coursereviews = None
    return coursereviews
