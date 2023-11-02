import os
import sys
import tqdm
from tqdm import tqdm
import pathlib
from zipfile import ZipFile
import shutil
import requests

def load_game():
	r = requests.get('https://raw.githubusercontent.com/alex-suspicious/Luminance/main/system/repositories.json')
	repo = r.json()
	return repo