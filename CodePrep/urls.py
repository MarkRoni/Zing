from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from CodePrep import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^disable_profile/$', views.disable_profile, name="disable_profile"),
    url(r'^reviewcourse/(?P<course_name_slug>[\w\-]+)/$', views.review_course,
        name='review_course'),
    url(r'^course/(?P<course_name_slug>[\w\-]+)/$',
        views.show_course, name='show_course'),
    url(r'^search/$', views.search_courses, name='search_course'),
    url(r'^search_results/$', views.search_results, name='search_results'),
    url(r'suggest/$', views.suggest, name='suggest'),
]
