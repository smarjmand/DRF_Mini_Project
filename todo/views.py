from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics, mixins
from .serializers import TodoSerializer, Todo, UserSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
User = get_user_model()


def main_page(request):
    return redirect('swagger-ui')

# ---------------------------------------------------------------
# to get all todos / create new _todo
#      ( by model-serializer as function-based-view )
@api_view(['GET', 'POST'])
def manage_todos_view(request: Request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        todo_deserializer = TodoSerializer(data=request.data)
        if todo_deserializer.is_valid():
            todo_deserializer.save()
            return Response(todo_deserializer.data, status=status.HTTP_201_CREATED)

    return Response(None, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------
# to read / update / delete a single_todo by id
#       ( by model-serializer as function-based-view )
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_view(reqeust: Request, todo_id: int):
    try:
        todo = Todo.objects.get(pk=todo_id)
    except Todo.DoesNotExist:
        return Response(None, status=status.HTTP_404_NOT_FOUND)

    if reqeust.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif reqeust.method == 'PUT':
        serializer = TodoSerializer(todo, reqeust.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_204_NO_CONTENT)
        return Response(None, status.HTTP_400_BAD_REQUEST)

    elif reqeust.method == 'DELETE':
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------
# to get all todos / create new _todo
#      ( by model-serializer as class-based-view )
class ManageTodosAPIView(APIView):

    def get(self, request: Request):
        todos = Todo.objects.all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response(todo_serializer.data, status.HTTP_200_OK)

    def post(self, request: Request):
        todo_deserializer = TodoSerializer(data=request.data)
        if todo_deserializer.is_valid():
            todo_deserializer.save()
            return Response(todo_deserializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------
# to read / update / delete a single_todo by id
#       ( by model-serializer as class-based-view )
class TodoDetailAPIView(APIView):
    def get_object(self, todo_id: int):
        try:
            todo = Todo.objects.get(pk=todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

    def get(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        todo_serializer = TodoSerializer(todo)
        return Response(todo_serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, todo_id: int):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)


# ---------------------------------------------------------------
# to get all todos / create new _todo
#       ( by model-serializer & mixins as class-based-view )

class ManageTodosMixinAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request: Request):
        return self.list(request)

    def post(self, request: Request):
        return self.create(request)


# ---------------------------------------------------------------
# to read / update / delete a single_todo by id
#       ( by model-serializer & mixins as class-based-view )
class TodoDetailMixinAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin, generics.GenericAPIView,
):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request: Request, pk):
        return self.retrieve(request, pk)

    def put(self, request: Request, pk):
        return self.update(request, pk)

    def delete(self, request: Request, pk):
        return self.destroy(request, pk)


# ---------------------------------------------------------------
# to get all todos / create new _todo
#       ( by model-serializer & Generics as class-based-view )
class MangeTodosGenericAPIView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


# ---------------------------------------------------------------
# to read / update / delete a single_todo by id
#       ( by model-serializer & Generics as class-based-view )
class TodoDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


# ---------------------------------------------------------------
# to read/create/update/delete
# ( by model-serializer & ViewSet as class-based-view )
class ManageTodosViewSetAPIView(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


# ---------------------------------------------------------------
# to see all users
#       ( by model-serializer & Generics as class-based-view )
class UserGenericAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
