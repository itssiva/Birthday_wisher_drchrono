from django.conf.urls import url, patterns


urlpatterns = patterns("Greeting.views",

                       url(r'custom$', 'customize_greeting', name='customize'),
                       url(r'^$', 'home', name='home'),
                       url(r'activate$', 'activate', name='activate'),
                       url(r'greeting_type', 'change_greeting_type', name='greeting_type'),
                       )


