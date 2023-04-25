from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Artist, User, Artwork, Collection, Favorite, Rating, Tag
from django.contrib.admin import widgets
from datetime import datetime

this_year = datetime.now().year

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('user', 'artist_role', 'description', 'profile_picture')


class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        artwork_tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
        fields = ('artwork_title', 'artwork_description', 'artwork_artist', 'artwork_picture', 'artwork_tag')


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        artwork = forms.ModelMultipleChoiceField(queryset=Artwork.objects.all())
        fields = ('collection_name', 'collection_artist', 'collection_description', 'artwork')



class FavoriteForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ('favorite_artist', 'favorite_artwork')


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating_level', 'rating_artist', 'rating_artwork')


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('tag_name', 'tag_description')


# for account creation
class CreateArtistAccountForm(forms.ModelForm):
    artist_role = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=True,
        initial=True
    )

    class Meta(ArtistForm.Meta):
        model = Artist
        fields = ('profile_picture', 'description', 'artist_role')


# for account creation
class CreateUserAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=False)
    last_name = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(max_length=60)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


# for account updating
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


# for account updating
class UpdateArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('description', 'profile_picture')


class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class DateInput (forms.DateInput):
    input_type = 'date'


class DateFilterForm(forms.Form):
    start_date = forms.DateField(label="Start Range", required=False, widget=forms.SelectDateWidget(years=range(2015, this_year+1), attrs={'style':'color:black'})) #, widget=widgets.AdminDateWidget)#, forms.TextInput(attrs={'style':'color:black'})})
    end_date = forms.DateField(label="End Range", required=False, widget=forms.SelectDateWidget(years=range(2015, this_year+1), attrs={'style':'color:black'})) #, widget=widgets.AdminDateWidget)#, forms.TextInput(attrs={'style':'color:black'})})
    view_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    filter_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    original_query = forms.CharField(max_length=500, widget=forms.HiddenInput, required=False)
    fields = '__all__'