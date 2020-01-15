from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
## これらはもう必要ない
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# @api_view()デコレータをつける
# @csrf_exempt
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
  """
  List all one snippets, or create a new snippet.
  """
  if request.method == 'GET':
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    ## JsonResponseをResponseに変更
    # return JsonResponse(serializer.data, safe=False)
    return Response(serializer.data)

  elif request.method == 'POST':
    ## JSONPerserを介さなくても良くなる
    # data = JSONParser().parse(request)
    # serializer = SnippetSerializer(data=data)
    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      ## JsonResponseをResponseに変更
      # return JsonResponse(serializer.data, status=201)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    ## JsonResponseをResponseに変更
    # return JsonResponse(serializer.errors, status=400)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
  """
  Retrieve, update or delete a code snippet.
  """
  try:
    snippet = Snippet.objects.get(pk=pk)
  except Snippet.DoesNotExist:
    ## HttpResponseをResponseに変更
    # return HttpResponse(status=404)
    return Response(status=status.HTTP_404_NOT_FOUND)

  if request.method == 'GET':
    serializer = SnippetSerializer(snippet)
    ## JsonResponseをResponseに変更
    # return JsonResponse(serializer.data)
    return Response(serializer.data)

  elif request.method == 'PUT':
    ## JSONParserを介さなくても良くなる
    # data = JSONParser().parse(request)
    # serializer = SnippetSerializer(snippet, data=data)
    serialiser = SnippetSerializer(snippet, data=request.data)
    if serializer.is_valid():
      serializer.save()
      ## JsonResponseをResponseに変更
      # return JsonResponse(serializer.data)
      return Response(serializer.data)
    ## JsonResponseをResponseに変更
    # return JsonResponse(serializer.errors, status=400)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == 'DELETE':
    snippet.delete()
    ## HttpResponseをResponseに変更
    # return HttpResponse(status=204)
    return Response(status=status.HTTP_204_NO_CONTENT)
