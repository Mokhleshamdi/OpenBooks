from django.urls import path

from django.contrib import admin
from django.conf.urls import url
from MyBook import views,forms

from django.conf import settings
from django.views.static import serve
from django.conf.urls import include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$',views.home),
    url(r'^([0-9]+)/$',views.details,name='details'),
    url(r'^details/([0-9]+)/$',views.delete,name='delete'),

    url(r'^ajouter/([0-9]+)/$',forms.UpdateView.as_view(),name='update'),
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    url(r'^ajouter/$', views.ajouter, name='ajouter'),
    url(r'^ajouter/back/$',views.back,name="back"),
    url(r'^$',views.login_view,name='login'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^like_book/$', views.like_book, name='like_book'),




    url(r'^update/(\d+)/$', views.Bookupdate,name="update"),
    url(r'^signIn/$',views.signIn,name="signIn"),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^user_update/([0-9]+)/$', views.User_update, name='User_update'),
    url(r'^user_list/([0-9]+)/$',views.delete_user,name='delete_user'),
    url(r'^user_search$', views.user_search, name="user_search"),
    url(r'^user_add$', views.user_add, name="user_add"),
    url(r'user_search', views.user_search, name='user_search'),
    url(r'borrow/([0-9]+)/$', views.book_borrow, name='book_borrow'),
    url(r'return/([0-9]+)/$', views.book_return, name='book_return'),
    url(r'comment/([0-9]+)/$', views.book_comment, name='book_comment'),

]


