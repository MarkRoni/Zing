from django.contrib import admin
from CodePrep.models import UserProfile, Subject, Provider, LearningStyle, Course, Review

admin.site.register(UserProfile)
admin.site.register(Subject)
admin.site.register(Provider)
admin.site.register(LearningStyle)
admin.site.register(Course)
admin.site.register(Review)
