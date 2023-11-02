import os
import sys
import tqdm
from tqdm import tqdm
import pathlib
from zipfile import ZipFile
import shutil
import requests
import base64
from aiohttp import web

current_game = []

def load_game():
	global current_game

	r = requests.get("https://raw.githubusercontent.com/alex-suspicious/Luminance/main/system/repositories.json")
	repo = r.json()

	for x in range(len(repo["list"])):
		game = repo["list"][x]
		exists = True

		for y in range( len(game[0]) ):
			if( not os.path.exists(game[0][y]) ):
				exists = False
				break

		if( exists ):			
			user = game[1].split("https://github.com/")[1].split("/")[0]
			name = game[1].split("https://github.com/")[1].split("/")[1]


			r = requests.get( f"https://raw.githubusercontent.com/{user}/{name}/main/info.json")
			data = r.json()
			print(data)
			current_game = data

			return str(current_game)

	return "none"

def getLogo():
	response = requests.get(current_game["game"]["logo"]).content
	return web.Response(body=response, content_type='image/*')

def getBackground():
	response = requests.get(current_game["game"]["backgrounds"][0]).content
	return web.Response(body=response, content_type='image/*')