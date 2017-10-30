from django.conf.urls import url
from . import views
urlpatterns = [
    #login START
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^login$', views.login),
    url(r'^create$', views.create),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    #login END

    url(r'^add_item', views.add_item),
    url(r'^create_item', views.create_item),
    url(r'^detail/(?P<id>\d+)$', views.detail),
    url(r'^add_list/(?P<id>\d+)$', views.add_list),
    url(r'^delete/(?P<product_id>\d+$)', views.delete),
    url(r'^remove_list/(?P<id>\d+$)', views.remove_list),
]