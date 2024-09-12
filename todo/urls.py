from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.ManageTodosViewSetAPIView)


urlpatterns = [
    path('', views.main_page),
    # function based views :
    path('fbv/all-todos', views.manage_todos_view),
    path('fbv/single-todo/<int:todo_id>', views.todo_detail_view),
    # class based views :
    path('cbv/all-todos', views.ManageTodosAPIView.as_view()),
    path('cbv/single-todo/<int:todo_id>', views.TodoDetailAPIView.as_view()),
    # mixins :
    path('mixin/all-todos', views.ManageTodosMixinAPIView.as_view()),
    path('mixin/single-todo/<pk>', views.TodoDetailMixinAPIView.as_view()),
    # generics :
    path('generic/all-todos', views.MangeTodosGenericAPIView.as_view()),
    path('generic/single-todo/<pk>', views.TodoDetailGenericAPIView.as_view()),
    # viewSets :
    path('viewset/all-todos/', include(router.urls)),
    # users / generics :
    path('current-user', views.UserGenericAPIView.as_view()),
]
