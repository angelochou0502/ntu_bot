from django.contrib import admin
from django.urls import path, include,re_path
from .views import NTUBotView
urlpatterns = [
	re_path(r'd4e395e5f388cbfcf3bb47b293ff5b560150148bafe42733a4/?$', NTUBotView.as_view())
    #path('',)
]