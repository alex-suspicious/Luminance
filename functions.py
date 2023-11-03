import os
import sys
import tqdm
from tqdm import tqdm
import pathlib
from zipfile import ZipFile
import shutil
import requests
import base64
import json
import bs4
from aiohttp import web
from bs4 import BeautifulSoup
 
current_game = []
repo = ""

def load_game():
	global current_game, repo

	if( os.path.exists("luminance_game") ):
		f = open("luminance_game", "r")
		splitted = f.read().split("<--->")
		current_game = json.loads( base64.b64decode( splitted[1] ) )
		f.close()

		repo = splitted[0]
		return str(current_game)

	r = requests.get("https://api.github.com/repos/alex-suspicious/Luminance/contents/system/repositories.json", verify=False)
	print(r.text)
	repo = json.loads( base64.b64decode( r.json()["content"] ) )

	for x in range(len(repo["list"])):
		game = repo["list"][x]
		exists = True

		for y in range( len(game[0]) ):
			if( not os.path.exists(game[0][y]) ):
				exists = False
				break

		if( exists ):
			#print(game)

			user = game[1].split("https://github.com/")[1].split("/")[0]
			name = game[1].split("https://github.com/")[1].split("/")[1]


			r = requests.get( f"https://api.github.com/repos/{user}/{name}/contents/info.json", verify=False)
			print(r.text)
			print(base64.b64decode( r.json()["content"] ))
			data = json.loads( base64.b64decode( r.json()["content"] ) )

			f = open("luminance_game", "w")
			f.write( game[1] + "<--->" + r.json()["content"] )
			f.close()

			repo = game[1]
			current_game = data

			return str(current_game)

	return "none"

def getLogo():
	response = requests.get(current_game["game"]["logo"], verify=False).content
	return web.Response(body=response, content_type='image/*')

def getBackground():
	response = requests.get(current_game["game"]["backgrounds"][0], verify=False).content
	return web.Response(body=response, content_type='image/*')

def getBackgrounds():
	return json.dumps(current_game["game"]["backgrounds"])

def getScreenshots():
	return json.dumps( current_game["screenshots"] )

def getGameName():
	return json.dumps( current_game["game"]["name"] )

def getCompatibility():
	return json.dumps( current_game["compatibility"] )

def getVersion():
	return json.dumps( current_game["version"] )

def getContributors():
	r = requests.get(repo, verify=False)
	print(r.text)
	soup = bs4.BeautifulSoup(r.text)
	contributors = []
	more = False

	users = soup.find_all("a", {"data-hovercard-type": "user"})
	for user in users:
		if( "github.com" in user["href"] ):
			if( not more ):
				more = True
				contributors = []

		if( more ):
			contributors.append( user["href"].replace("https://github.com","") )
		else:
			contributors.append( user["href"] )

	return json.dumps(contributors)
		