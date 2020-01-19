from django.urls import path, re_path
from . import views


urlpatterns = [
    # deprecated versions
    # FBV's
    # path('', views.index, name='main_board'),
    # path('<int:board_id>/', views.topics, name='topics') # non regex ver
    # re_path(r'^(?P<board_id>\d+)/new', views.new_topic, name='new_topic'),
    # re_path(r'^(?P<board_id>\d+)/topics/(?P<topic_id>\d+)/reply', views.post_reply, name='post_reply'),
    # re_path(r'^(?P<board_id>\d+)/topics/(?P<topic_id>\d+)/', views.topic_detail, name='topic_detail'),
    # re_path(r'^(?P<board_id>\d+)/', views.topics, name='topics'),

    # CBV version
    path('', views.BoardListView.as_view(), name='main_board'),
    re_path(r'^(?P<board_id>\d+)/new', views.TopicCreateView.as_view(), name='new_topic'),
    re_path(r'^(?P<board_id>\d+)/topics/(?P<topic_id>\d+)/reply/(?P<post_id>\d+)/edit',
            views.PostUpdateView.as_view(), name='post_edit'),
    re_path(r'^(?P<board_id>\d+)/topics/(?P<topic_id>\d+)/reply', views.PostReplyView.as_view(), name='post_reply'),
    re_path(r'^(?P<board_id>\d+)/topics/(?P<topic_id>\d+)/', views.PostListView.as_view(), name='topic_detail'),
    re_path(r'^(?P<board_id>\d+)/', views.TopicListView.as_view(), name='topics'),

]