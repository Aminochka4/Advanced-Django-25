import logging 
from rest_framework.viewsets import ModelViewSet 
from .models import User, Project, Category, Priority, Task 
from .serializers import UserSerializer, ProjectSerializer, CategorySerializer, PrioritySerializer, TaskSerializer 
from rest_framework.permissions import IsAuthenticated 
from django.shortcuts import render
from .permissions import IsAdmin, IsManager, IsEmployee
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]  # Only admins can manage users

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsManager]  # Managers can manage projects

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsEmployee]  # Employees can manage their tasks

def index(request):
    return render(request, 'index.html')
logger = logging.getLogger(__name__)  

class UserViewSet(ModelViewSet): 
    queryset = User.objects.all() 
    serializer_class = UserSerializer 

class ProjectViewSet(ModelViewSet): 
    queryset = Project.objects.all() 
    serializer_class = ProjectSerializer 
 
class CategoryViewSet(ModelViewSet): 
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer 

class PriorityViewSet(ModelViewSet): 
    queryset = Priority.objects.all() 
    serializer_class = PrioritySerializer 

class TaskViewSet(ModelViewSet): 
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer 
    filter_backends = [DjangoFilterBackend, SearchFilter] 
    filterset_fields = ['project', 'priority', 'category'] 
    search_fields = ['title', 'description']
    
    def perform_create(self, serializer): 
        logger.info("Creating a new task") 
        serializer.save() 

class TaskViewSet(ModelViewSet): 
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer 
    permission_classes = [IsAuthenticated]