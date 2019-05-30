import math

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board


def index(request):
    listsize, pagesize = 3, 3

    currentpage = 1 if request.GET.get('p') is None else int(request.GET.get('p'))

    # 1. 페이징을 위한 기본데이터 계산
    totalcount = Board.objects.count()
    pagecount = math.ceil(totalcount/listsize)
    blockcount = 0
    currentblock = math.ceil(currentpage.pagesize)

    # 3. 페이지 리스트를 그리기 위한 데이터 값
    beginpage = 0
    prevpage = 0
    nextpage = 0
    endpage = 0

    startindex = (currentpage-1)*listsize
    board_list = Board.objects.all().order_by('-id')[startindex:startindex+listsize]

    data = {
        'board_list': board_list,
        'currentpage': currentpage
    }
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

    board.hit += 1
    board.save()

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
    try:
        board = Board.objects.get(id=request.POST['id'], user_id=request.session['authuser']['id'])
    except Exception:
        return HttpResponseRedirect('/')

    board.title = request.POST['title']
    board.contents = request.POST['contents']

    board.save()
    return HttpResponseRedirect('/board/view?id=' + request.POST['id'])


def delete(request):
    try:
        board = Board.objects.get(id=request.GET['id'], user_id=request.session['authuser']['id'])
    except Exception:
        return HttpResponseRedirect('/')

    board.delete()
    return HttpResponseRedirect('/board')
