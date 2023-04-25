from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# Here we override the default User model
# to add more fields dedicated to that Artist.
# Django already has these fields included for users: id PK, password,
# is_superuser, username, last_name, email, is_staff, is_active, first_name

# These can be accessed like: u = User.objects.get(username='mayalanger')

# For more details:
# https://stackoverflow.com/questions/42478191/django-how-to-add-an-extra-field-in-user-model-and-have-it-displayed-in-the-adm/42481381
# https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#extending-the-existing-user-model
class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    artist_role = models.BooleanField(default=False)
    description = models.TextField(max_length=280, null=True, blank=True)  # this is the default for all descriptions

    # https://www.geeksforgeeks.org/python-uploading-images-in-django/

    # to user this, we need to install Pillow.  "python -m pip install Pillow" or
    # download it at https://pypi.org/project/Pillow/
    # "the Python Imaging Library adds image processing capabilities to your Python interpreter"
    #  - https://pypi.org/project/Pillow/
    profile_picture = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.user}'


# Tags can be added to Artwork.
class Tag(models.Model):
    # tag_id is not needed as a field on this file.  It can be referenced by other models.
    tag_name = models.CharField(max_length=50)
    tag_description = models.TextField(max_length=280, null=True, blank=True)

    def __str__(self):
        return f'{self.tag_name}'


# This is the Model representing a piece of Artwork (not specifically a submission of a piece)
class Artwork(models.Model):
    # artwork_id this is not needed as a field on this file.  It can be referenced by other models.
    artwork_title = models.CharField(max_length=200)
    artwork_description = models.TextField(max_length=280, null=True, blank=True)
    # One piece of Artwork can have multiple Artists
    # Do to this, deletion of an artist does not delete the Artwork.
    # All information about the Artwork including Favorites, what Collection, and Ratings are preserved.
    # However, Artists can reclaim work.
    # artwork_artist = models.ManyToManyField(Artist)
    artwork_artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    # One piece of Artwork can have multiple Tags
    artwork_tag = models.ManyToManyField(Tag, blank=True)
    artwork_picture = models.ImageField(upload_to='images/', null=True, blank=True)  # comment out null and blank later
    artwork_created = models.DateTimeField()

    def __str__(self):
        return f'{self.artwork_title}'


# Each Collection has many pieces of Artwork inside it.  A Collection is
# created by one User.
class Collection(models.Model):
    # collection_id is not needed as a field on this file.  It can be referenced by other models.
    collection_name = models.CharField(max_length=200)
    collection_description = models.TextField(max_length=280, null=True, blank=True)
    # this collection will cease to exist when an Artist deletes their account.
    collection_artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    # this collection will have many pieces of Artwork inside it.
    artwork = models.ManyToManyField(Artwork, blank=True)

    def __str__(self):
        return f'{self.collection_name}'


# Many-to-Many relationship may not work; definitions have to
# be in a certain order.
# Each Favorites folder has one Artist and many pieces of Artwork.
class Favorite(models.Model):
    favorite_artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    # A Favorite folder can have no submissions in it so far.
    favorite_artwork = models.ForeignKey('Artwork', on_delete=models.CASCADE)

    # for now, just the user's username is displayed.
    def __str__(self):
        return f'{self.favorite_artist.user}'


# Each Artist can rate a piece of Artwork
# For Django, creating a model is a valid way to do things.
# We can edit this as we go.

# https://stackoverflow.com/questions/45842245/implement-a-multi-part-5-star-rating-system-in-django-1-11
class Rating(models.Model):
    rating_level = models.IntegerField(default=1, validators=(MaxValueValidator(5), MinValueValidator(1)))
    rating_artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    rating_artwork = models.ForeignKey('Artwork', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rating_artwork.artwork_title, self.rating_level, self.rating_artist.user}'
class ArtworkSummary(Artwork):
    class Meta:
        proxy = True
        verbose_name = 'Artwork Summary'
        verbose_name_plural = 'Artwork Summary'