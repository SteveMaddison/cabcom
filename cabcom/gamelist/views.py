from django.shortcuts import render, get_object_or_404
from cabcom.gamelist.models import Data, Game

def index(request):
	context = {
		'first': 1,
		'last':  Game.objects.count(),
		'games': Game.objects.all(),
	}
	return render(request, 'gamelist/index.html', context)

def detail(request, game_id):
	game = get_object_or_404(Game, pk=game_id)
	return render(request, 'gamelist/detail.html', {'game': game})

