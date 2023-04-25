from . import views
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import contact_us, success_message

app_name = 'gallery'

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    re_path(r'^landing_page/$', views.landing_page, name='landing_page'),
    path('artist_list', views.artist_list, name='artist_list'),
    path('artist/create/', views.artist_new, name='artist_new'),
    path('artist/<int:pk>/edit/', views.artist_edit, name='artist_edit'),
    path('artist/<int:pk>/delete/', views.artist_delete, name='artist_delete'),
    path('artist/<int:pk>/', views.artist_view, name='artist_view'),
    path('artwork_list', views.artwork_list, name='artwork_list'),
    path('artwork/create/', views.artwork_new, name='artwork_new'),
    path('artwork/<int:pk>/edit/', views.artwork_edit, name='artwork_edit'),
    path('artwork/<int:pk>/details/', views.artwork_details, name='artwork_details'),
    path('artwork/<int:pk>/delete/', views.artwork_delete, name='artwork_delete'),
    path('collection_list', views.collection_list, name='collection_list'),
    path('collection/<int:pk>/', views.collection_view, name='collection_view'),
    path('collection/create/', views.collection_new, name='collection_new'),
    path('collection/<int:pk>/edit/', views.collection_edit, name='collection_edit'),
    path('collection/<int:pk>/delete/', views.collection_delete, name='collection_delete'),
    path('favorite_list', views.favorite_list, name='favorite_list'),
    path('artwork_list', views.artwork_list, name='rating_list'),
    path('tag_list', views.tag_list, name='tag_list'),
    path('tag/create/', views.tag_new, name='tag_new'),
    path('tag/<int:pk>/edit/', views.tag_edit, name='tag_edit'),
    path('tag/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
    path('create_account', views.create_account, name='create_account'),
    path('account_details', views.account_details, name='account_details'),
    path('account/<int:pk>/<int:pk_alt>/edit', views.update_account_details, name='update_account_details'),
    path('account/<int:pk>/edit', views.user_update_account_details, name='user_update_account_details'),
    path('account/<int:pk>/delete', views.user_delete_account, name='user_delete_account'),
    path('favorite/<int:pk>', views.favorite_new, name='favorite_new'),
    path('rating/<int:pk>/<int:level>', views.rating_new, name='rating_new'),
    path('search/', views.search_results, name='search_results'),
    path('search/<int:view_id>/', views.search_results, name='search_results'),
    path('search/<int:view_id>/<original_query>/', views.search_results, name='search_results'),
    path('search/<int:view_id>/<int:filter_id>/<original_query>/', views.search_results, name='search_results'),
    path('contact/', contact_us, name='contact_us'),
    path('success/', success_message, name='success_message'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('account/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()