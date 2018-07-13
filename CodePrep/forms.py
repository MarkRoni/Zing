from django import forms
from CodePrep.models import UserProfile, Review, Course, LearningStyle

# Form used during signup for custom profile data
# Also displayed on user profile for fast profile update
class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        # Hide username and enrolled courses so they're not displayed on profile
        exclude = ('user', 'enrolledcourses')

# Form used to submit a review of a course
class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(initial=0,
        help_text="Please rate your experience from 1 to 5.",
        min_value=0, max_value=5)
    comment = forms.CharField(max_length=5000,
        help_text="Tell us what you thought about the course.")

    class Meta:
        model = Review
        fields = ('rating','comment',)

# Form used to search for course(s)
# Supports search terms based on coding language
# Supports filters for learning style, price
# Supports ordering of results by average rating
class SearchForm(forms.ModelForm):
    subject = forms.CharField(max_length=50,
            help_text="What do you want to learn about?",
            widget=forms.TextInput(
                attrs={'placeholder':'Subject Search'}
            ))
    style = forms.ModelMultipleChoiceField(
            queryset=LearningStyle.objects.all(),
            required=False, to_field_name="id",
            widget=forms.CheckboxSelectMultiple(
                attrs={'class':"learning-style-select"}
            ),
            help_text="What style of course suits you best?")
    price = forms.BooleanField(required=False,
            widget=forms.CheckboxInput(),
            help_text="Only search free courses?")
    orderchoices = (('rating','Ascending'),('-rating','Descending'))
    order = forms.ChoiceField(choices=orderchoices,
            help_text="Order by Rating: ")

    class Meta:
        model = Course
        fields = ('subject', 'style', 'price')
