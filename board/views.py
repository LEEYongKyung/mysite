from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board


def index(request):
    # board_list = Board.objects.all().order_by('-regdate')
    # for board in board_list:
    #     print(board.id, board.title, board.user)

    return render(request, 'board/index.html')


def write(request):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/')

    return render(request, 'board/write.html')






def create(request):
    board = Board()
    board.title = 'test'
    board.contents = 'test'
    board.user_id = 1

    board.save()

    return HttpResponse('ok')


def readone(request):
    # /board/view?id=4
    board = Board.objects.get(id=4)
    print(board.id, board.title, board.contents, board.user.name)
    return HttpResponse('ok')


def update(request):
    board = Board.objects.get(id=4)
    board.title = 'hello'
    board.contents = 'hello'

    board.save()

    return HttpResponse('ok')


def delete(request):
    board = Board.objects.get(id=4)
    board.delete()

    return HttpResponse('ok')
