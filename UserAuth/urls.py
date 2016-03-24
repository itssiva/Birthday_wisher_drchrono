from django.conf.urls import url, patterns


urlpatterns = patterns('UserAuth.views',
                       url(r'^login/$', 'start_login', name='login'),
                       url(r'^logout/$', 'user_logout', name='logout'),
                       url(r'authorize_callback/', 'authorization_callback'),
                       )

