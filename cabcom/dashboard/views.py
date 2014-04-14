from django.shortcuts import render
from django.http import HttpResponse
from cabcom.gamelist.models import Data, Game

def index(request):
	context = {
		'data_count': Data.objects.count(),
		'game_count': Game.objects.count(),
	}
	return render(request, 'dashboard/index.html', context)
