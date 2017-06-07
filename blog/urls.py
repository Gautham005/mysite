from django.conf.urls import url

from blog import views
from blog.views import home, add_post
from blog.views import post_detail

urlpatterns = [
    url(r'^$', home, name="home"),
    url(r'^add/$', add_post,name="add_post"),
    url(r'^(?P<no>[0-9]+)/$', post_detail,name="post"),
    url(r'^(?P<no>[0-9]+)/edit', edit_detail, name="edit_post"),
    url(r'^(?P<no>[0-9]+)/delete', delete_detail, name="delete_post"),
]
