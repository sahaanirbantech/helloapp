from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'^hello/(?P<uname>.*)$',
        views.get_put_username,
        name='get_put_username'
    ),
    url(r'^health-check?$', 
        views.health_check
    )
]
