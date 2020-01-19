from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.views.generic import UpdateView, ListView, CreateView
from .models import Board, Topic, Post
from .forms import NewTopic, NewReply
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator


def index(r):   # deprecated; replaced with BoardListView
    b = Board.objects.all()
    return render(r, 'messageboard.html', {'boards': b})


def topics(r, board_id):
    b = get_object_or_404(Board, pk=board_id)
    t = b.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(r, 'topics.html', {'board': b, 'topics': t})


@login_required
def new_topic(r, board_id):
    b = get_object_or_404(Board, pk=board_id)
    u = r.user
    if r.method == 'POST':
        f = NewTopic(r.POST)
        if f.is_valid():
            t = f.save(commit=False)
            t.board = b
            t.started_by = u
            t.save()
            p = Post.objects.create(
                message=f.cleaned_data.get('message'),
                topic=t,
                created_by=u
            )
            return redirect('topic_detail', board_id=board_id, topic_id=t.pk)
    else:
        f = NewTopic()
    return render(r, 'new_topic.html', {'board': b, 'form': f})

# raw form call v1
# def new_topic(r, board_id):
#     b = get_object_or_404(Board, pk=board_id)
#
#     if r.method == "POST":
#         s = r.POST['p_subject']
#         m = r.POST['p_message']
#
#         u = User.objects.first()
#
#         t = Topic.objects.create(
#             subject=s,
#             board=b,
#             started_by=u
#         )
#
#         p = Post.objects.create(
#             topic=t,
#             message=m,
#             created_by=u
#         )
#
#         return redirect('topics', board_id=board_id)
#     return render(r, 'new_topic.html', {'board': b})


def topic_detail(r, board_id, topic_id):
    t = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    t.views += 1
    t.save()
    return render(r, 'topic_detail.html', {'topic': t})


def post_reply(r, board_id, topic_id):
    t = get_object_or_404(Topic, board__pk=board_id, pk=topic_id)
    u = r.user
    if r.method == 'POST':
        f = NewReply(r.POST)
        if f.is_valid():
            p = f.save(commit=False)
            p.topic = t
            p.created_by = u
            p.save()
            return redirect('topic_detail', board_id=board_id, topic_id=topic_id)
    else:
        f = NewReply()
    return render(r, 'post_reply.html', {'topic': t, 'form': f})


class BoardListView(ListView):  # replacement CBV for FBV views.index()
    model = Board
    context_object_name = 'boards'
    template_name = 'messageboard.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('board_id'))
        qs = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return qs


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_detail.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic,board__pk=self.kwargs.get('board_id'), pk=self.kwargs.get('topic_id'))
        qs = self.topic.posts.order_by('created_date')
        return qs


@method_decorator(login_required, name='dispatch')
class TopicCreateView(CreateView):
    model = Topic   # bind to Model from models.py
    form_class = NewTopic   # bind to Form from forms.py
    template_name = 'new_topic.html'
    pk_url_kwarg = 'topic_id'   # used to match keyword argument in urls.py
    context_object_name = 'topic'   # used by dtl's {% rendertags %}

    def form_valid(self, f):
        board_id = self.kwargs.get('board_id')

        t = f.save(commit=False)
        t.board = get_object_or_404(Board, pk=board_id) # bind foreign key
        t.started_by = self.request.user
        t.save()
        p = Post.objects.create(
            message=f.cleaned_data.get('message'),
            topic=t,
            created_by=self.request.user
        )
        return redirect('topic_detail', board_id=board_id, topic_id=t.pk)

    def get_context_data(self, **kwargs):
        board_id = self.kwargs.get('board_id')
        kwargs['board'] = get_object_or_404(Board, pk=board_id)  # used by dtl's {% rendertags %}
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class PostReplyView(CreateView):
    model = Post
    form_class = NewReply
    # fields = ('message',)
    template_name = 'post_reply.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        topic_id = self.kwargs.get('topic_id')
        p = form.save(commit=False)
        p.topic = get_object_or_404(Topic, pk=topic_id)
        p.created_by = self.request.user
        t = p.topic
        t.last_updated = timezone.now()
        p.save()
        t.save()
        board_id = p.topic.board.pk
        return redirect('topic_detail', board_id=board_id, topic_id=topic_id)

    def get_context_data(self, **kwargs):
        topic_id = self.kwargs.get('topic_id')
        kwargs['topic'] = get_object_or_404(Topic, pk=topic_id)  # used by dtl's {% rendertags %}
        return super().get_context_data(**kwargs)


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    form_class = NewReply   # can use a form
    # fields = ('message', )    # or this, since all the data needed is in one table
    template_name = 'post_edit.html'
    pk_url_kwarg = 'post_id'    # keyword arg name used in urls.py
    context_object_name = 'post'

    def form_valid(self, form):
        p = form.save(commit=False)
        p.updated_by = self.request.user
        p.updated_date = timezone.now()
        t = p.topic
        t.last_updated = timezone.now()
        p.save()
        t.save()
        return redirect('topic_detail', board_id=p.topic.board.pk, topic_id=p.topic.pk)
