from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from .models import Todo
from .serializers   import TodoSerializer 


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        "all todo": '/api/todo',
        "create todo": '/api/todo/',
        "update todo": '/api/todo/pk',
        "delete todo": '/api/todo/pk/delete',
    }
    return Response(api_urls)

@api_view(['GET','POST'])
def add_todo(request):
    todo = TodoSerializer(data=request.data)

    #validate for already existing data
    if Todo.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
    if todo.is_valid():
        todo.save()
        return Response(todo.data, status=status.HTTP_201_CREATED)
    else:
        return Response(todo.errors, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def view_todo(request):
    #checking for the parameters from the url
    if request.query_params :
        todos = Todo.objects.filter(**request.query_params.dict())
    else:
        todos = Todo.objects.all()
    
    #if there is something in todo else raise error
    if todos:
        serializer = TodoSerializer(todos,many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
def update_todo(request,pk):
    todo = Todo.objects.get(pk=pk)
    serializer = TodoSerializer(instance=todo,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['DELETE'])
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return Response(status=status.HTTP_202_ACCEPTED)