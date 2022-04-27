import wget
import requests

output_directory = 'C:/Users/Alberto/Desktop/Workspace/django_api/api/al_games/templates/media' 



url = "https://www.ludonauta.es/files/ludico/juegos-mesas/juego-mesa-sequence-1982-933240464.jpg"
filename = wget.download(url -nc)
