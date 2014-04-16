from django.http import Http404
from django.shortcuts import render, get_object_or_404
from cabcom.gamelist.models import Data, Game

def index(request, object_type):
	if object_type == 'game':
		title = 'Game List'
		items = Game.objects.all()[0:49]
		count = Game.objects.count()
	elif object_type == 'data':
		title = 'Game Database'
		items = Data.objects.all()[0:49]
		count = Data.objects.count()
	else:
		raise Http404

	context = {
		'title' : title,
		'first' : 1,
		'last'  :  50,
		'count' : count,
		'games' : items,
		'object_type': object_type,
	}

	return render(request, 'gamelist/index.html', context)

def detail(request, object_type, game_id):
	if object_type == 'game':
		game = get_object_or_404(Game, pk=game_id)
	elif object_type == 'data':
		game = get_object_or_404(Data, pk=game_id)
	else:
		raise Http404

	return render(request, 'gamelist/detail.html', {'game': game})

