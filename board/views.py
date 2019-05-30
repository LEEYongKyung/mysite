from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board


def index(request):
    board_list = Board.objects.all().order_by('-regdate')
    data = {'board_list': board_list}
    return render(request, 'board/index.html', data)


def write(request):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/')

    return render(request, 'board/write.html')


def add(request):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/')

    board = Board()
    board.title = request.POST['title']
    board.contents = request.POST['contents']
    board.user_id = request.session['authuser']['id']

    board.save()

    return HttpResponseRedirect('/board')


def view(request):
    board_id = request.GET['id']
    board = Board.objects.get(id=board_id)
    data = {'board': board}
    return render(request, 'board/view.html', data)


def updateform(request):
    board_id = request.GET['id']
    try:
        board = Board.objects.get(id=board_id, user_id=request.session['authuser']['id'])
    except Exception :
        return HttpResponseRedirect('/')

    data = {'board': board}
    return render(request, 'board/updateform.html', data)


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
