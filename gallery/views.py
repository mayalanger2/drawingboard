from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db.models import Avg
from django.template import Template, Context
from django.template.loader import get_template

now = timezone.now()


def landing_page(request):
    return render(request, 'gallery/landing_page.html',
                  {'gallery': landing_page})


def home(request):
    artwork = Artwork.objects.all()
    allart = {'artworks': artwork}
    homefinal = {'gallery': home}
    return render(request, 'gallery/home.html', allart)


# if account is created successfully, user will be automatically logged in and redirected to home page
def create_account(request):
    if request.method == "POST":
        user_form = CreateUserAccountForm(request.POST)
        artist_form = CreateArtistAccountForm(request.POST, request.FILES)
        if user_form.is_valid() and artist_form.is_valid():
            newuser = user_form.save()
            artist = artist_form.save(commit=False)
            artist.user = newuser
            artist.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('gallery:home')
    else:
        user_form = CreateUserAccountForm()
        artist_form = CreateArtistAccountForm
    return render(request, 'registration/create_account.html',
                  {'user_form': user_form, 'artist_form': artist_form})


def account_details(request):
    return render(request, 'registration/account_details.html',
                  {'registration': account_details})


def update_account_details(request, pk, pk_alt):
    user_account = get_object_or_404(User, pk=pk)
    artist_account = get_object_or_404(Artist, pk=pk_alt)
    if request.method == "POST":
        # update
        user_form = UpdateUserForm(request.POST, instance=user_account)
        artist_form = UpdateArtistForm(request.POST, request.FILES, instance=artist_account)
        if user_form.is_valid() and artist_form.is_valid():
            user_account = user_form.save(commit=False)
            artist_account = artist_form.save(commit=False)
            user_account.updated_date = artist_account.updated_date = timezone.now()
            user_account.save()
            artist_account.save()
            return redirect('gallery:account_details')
    else:
        # edit
        user_form = UpdateUserForm(instance=user_account)
        artist_form = UpdateArtistForm(instance=artist_account)
    return render(request, 'registration/update_account_details.html', {
        'user_form': user_form,
        'artist_form': artist_form
    })


def user_update_account_details(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        # update
        user_form = UpdateUserForm(request.POST, instance=user)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.updated_date = timezone.now()
            user.save()
            return redirect('gallery:account_details')
    else:
        # edit
        user_form = UpdateUserForm(instance=user)
    return render(request, 'registration/update_account_details.html', {'user_form': user_form})


def user_delete_account(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('gallery:home')


def artist_list(request):
    artist = Artist.objects.all()
    return render(request, 'gallery/artist_list.html',
                  {'artists': artist})


def artist_view(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    artworks = Artwork.objects.filter(artwork_artist=artist)
    context = {'artist': artist, 'artworks': artworks}
    return render(request, 'gallery/artist_view.html', context)


def artist_new(request):
    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.created_date = timezone.now()
            artist.save()
            return redirect('gallery:artist_list')
    else:
        form = ArtistForm()
        # print("Else")
    return render(request, 'gallery/artist_new.html', {'form': form})


def artist_edit(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == "POST":
        # update
        form = ArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            artist = form.save(commit=False)
            artist.updated_date = timezone.now()
            artist.save()
            return redirect('gallery:artist_list')
    else:
        # edit
        form = ArtistForm(instance=artist)
    return render(request, 'gallery/artist_edit.html', {'form': form})


def artist_delete(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    artist.delete()
    return redirect('gallery:artist_list')


def artwork_list(request):
    artwork = Artwork.objects.all()
    return render(request, 'gallery/artwork_list.html',
                  {'artworks': artwork})


def artwork_new(request):
    if request.method == "POST":
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.created_date = timezone.now()
            artwork.save()

            return redirect('gallery:artwork_list')
    else:
        form = ArtworkForm()
        # print("Else")
    return render(request, 'gallery/artwork_new.html', {'form': form})


def artwork_edit(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    if request.method == "POST":
        # update
        form = ArtworkForm(request.POST, request.FILES, instance=artwork)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.updated_date = timezone.now()
            artwork.save()
            form.save_m2m()
            return redirect('gallery:artwork_list')
    else:
        # edit
        form = ArtworkForm(instance=artwork)
    return render(request, 'gallery/artwork_edit.html', {'form': form})


def artwork_details(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    # Book.objects.all().aggregate(Avg('price'))
    # {'price__avg': 34.35}
    avgfull = Rating.objects.filter(rating_artwork=artwork).aggregate(Avg('rating_level')).get('rating_level__avg', 0.0)
    if avgfull is not None:
        avg = round(avgfull, 2)
    else:
        avg = avgfull
    try:
        # if favorite exists
        favorite = Favorite.objects.get(favorite_artist=request.user.artist, favorite_artwork=artwork)
        try:
            rating = Rating.objects.get(rating_artist=request.user.artist, rating_artwork=artwork)
            rating = rating.rating_level
        except Rating.DoesNotExist:
            rating = "not rated yet!"
        return render(request, 'gallery/artwork_details.html',
                      {'artwork': artwork, 'status': 'button heart red', 'avgrate': avg, 'prevrate': rating})
    except Favorite.DoesNotExist:
        try:
            rating = Rating.objects.get(rating_artist=request.user.artist, rating_artwork=artwork)
            rating = rating.rating_level
        except Rating.DoesNotExist:
            rating = "Not rated yet!"
        return render(request, 'gallery/artwork_details.html', {'artwork': artwork, 'status': '', 'avgrate': avg, 'prevrate': rating})
    except:
        return render(request, 'gallery/artwork_details.html', {'artwork': artwork, 'avgrate': avg})


def artwork_delete(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)
    artwork.delete()
    return redirect('gallery:artwork_list')


def send_email(request):
    # add send e-mail confirmation
    # set up the subject, message, and user’s email address
    subject = ''
    message = ''
    user = request.user  # request was passed to the method as a parameter for the view
    user_email = user.email  # pull user’s email out of the user record
    # try to send the e-mail – note you can send to multiple users – this just sends
    # to one user.
    try:
        send_mail(subject, message, 'groupsevenweb@gmail.com', [user_email])
        sent = True
    except:
        print("Error sending e-mail")


def collection_list(request):
    collection = Collection.objects.all()
    return render(request, 'gallery/collection_list.html',
                  {'collections': collection})


def collection_view(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    artworks = collection.artwork.all()
    artist = collection.collection_artist
    return render(request, 'gallery/collection_view.html',
                  {'artworks': artworks, 'collection': collection, 'artist': artist})


def collection_new(request):
    if request.method == "POST":
        form = CollectionForm(request.POST, request.FILES)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.created_date = timezone.now()
            collection.save()
            form.save_m2m()
            return redirect('gallery:collection_list')
    else:
        form = CollectionForm()
        # print("Else")
    return render(request, 'gallery/collection_new.html', {'form': form})


def collection_edit(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == "POST":
        # update
        form = CollectionForm(request.POST, request.FILES, instance=collection)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.updated_date = timezone.now()
            collection.save()
            form.save_m2m()
            return redirect('gallery:collection_list')
    else:
        # edit
        form = CollectionForm(instance=collection)
    return render(request, 'gallery/collection_edit.html', {'form': form})


def collection_delete(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    collection.delete()
    return redirect('gallery:collection_list')


def favorite_new(request, pk):
    artwork = get_object_or_404(Artwork, pk=pk)

    try:
        favorite_instance = Favorite.objects.get(favorite_artist=request.user.artist, favorite_artwork=artwork)
        favorite_instance.delete()
    except Favorite.DoesNotExist:
        favorite_instance = Favorite.objects.create(favorite_artist=request.user.artist, favorite_artwork=artwork)
        favorite_instance.save()

    return redirect('gallery:home')


def search_results(request, view_id=3, filter_id=None, start_date=None, end_date=None, original_query=None):
    query = request.GET.get('q')
    # artwork = Artwork.objects.all()
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            filter_id = filter_id
            view_id = view_id
            original_query = original_query
    else:
        form = DateFilterForm()
    if original_query:
        try:
            query = original_query
            object_list = Artwork.objects.filter(
                Q(artwork_title__icontains=query) | Q(artwork_description__icontains=query) |
                Q(artwork_tag__tag_name__icontains=query)
            )
            object_list = object_list.all().order_by('artwork_created')
            sorted_by = "Date Submitted (oldest first)"
            if view_id == 2:
                object_list = object_list.all().order_by('-artwork_created')
                sorted_by = "Date Submitted (newest first)"
            elif view_id == 4:
                object_list = object_list.all().order_by('artwork_title')
                sorted_by = "Artwork Title (A to Z)"
            elif view_id == 5:
                object_list = object_list.all().order_by('-artwork_title')
                sorted_by = "Artwork Title (Z to A)"
            if filter_id == 1:
                if start_date and end_date:
                    object_list = object_list.filter(Q(artwork_created__gte=start_date, artwork_created__lte=end_date))
                elif start_date:
                    object_list = object_list.filter(Q(artwork_created__gte=start_date))
                elif end_date:
                    object_list = object_list.filter(Q(artwork_created__lte=end_date))
        except Artwork.DoesNotExist:
            object_list = None
        return render(request, 'gallery/search_results.html', {'object_list': object_list, 'query': query,
                                                               'sorted_by': sorted_by, 'view_id': view_id, 'form': form,
                                                               'start_filter': start_date, 'end_filter': end_date, 'filter_id': filter_id})
    else:
        try:
            object_list = Artwork.objects.filter(
                Q(artwork_title__icontains=query) | Q(artwork_description__icontains=query) |
                Q(artwork_tag__tag_name__icontains=query)
            )
            object_list = object_list.all().order_by('artwork_created')
            sorted_by = "Date Submitted (oldest first)"
        except Artwork.DoesNotExist:
            object_list = None
        return render(request, 'gallery/search_results.html', {'object_list': object_list, 'query': query,
                                                               'sorted_by': sorted_by, 'view_id': view_id, 'form': form,
                                                               'start_filter': start_date, 'end_filter': end_date, 'filter_id': filter_id})


def favorite_list(request):
    favorite = Favorite.objects.all()
    return render(request, 'gallery/favorite_list.html',
                  {'favorites': favorite})


def rating_new(request, pk, level):
    artwork = get_object_or_404(Artwork, pk=pk)

    try:
        rating_instance = Rating.objects.get(rating_artist=request.user.artist, rating_artwork=artwork)
        rating_instance.delete()
        rating_new_instance = Rating.objects.create(rating_artist=request.user.artist, rating_artwork=artwork,
                                                    rating_level=level)
        rating_new_instance.save()
    except Rating.DoesNotExist:
        rating_instance = Rating.objects.create(rating_artist=request.user.artist, rating_artwork=artwork,
                                                rating_level=level)
        rating_instance.save()

    return redirect('gallery:home')


def tag_list(request):
    tag = Tag.objects.all()
    return render(request, 'gallery/tag_list.html',
                  {'tags': tag})


def tag_new(request):
    if request.method == "POST":
        form = TagForm(request.POST, request.FILES)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.created_date = timezone.now()
            tag.save()

            return redirect('gallery:tag_list')
    else:
        form = TagForm()
        # print("Else")
    return render(request, 'gallery/tag_new.html', {'form': form})


def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return redirect('gallery:tag_list')


def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        # update
        form = TagForm(request.POST, request.FILES, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.save()
            return redirect('gallery:tag_list')
    else:
        # edit
        form = TagForm(instance=tag)
    return render(request, 'gallery/tag_edit.html', {'form': form})


def contact_us(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            user = request.user
            message = "Sent by: "+ user.email + "\nFirst name: " + user.first_name + "\nLast name: " + user.last_name + "\nMessage: " + message
            try:
                send_mail(subject, message, user, ['groupsevenweb@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('gallery:success_message')
    return render(request, 'gallery/contact_us.html', {'form': form})


def success_message(request):
    return render(request,'gallery/success_message.html')