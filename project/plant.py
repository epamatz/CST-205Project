import base64
import requests
from time import sleep
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename
import cv2
import wikipedia
import secret_access_key as secret_access_key

img = 'calla_lily.jpg'
img = 'gloriosa.jpg'
imgName = 'Calla lily'
imgName = 'Gloriosa superba'

path = ' -- path to the static folder provided -- '

link = imgName.replace(' ', '_')

reg_img = 'reg_' + img
image = cv2.imread(img)
cv2.imwrite(path + reg_img, image)

cb_image = 'cb_' + img
image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
cv2.imwrite(path + cb_image, image)

uv_image = 'uv_' + img
image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
uimage = cv2.applyColorMap(image, cv2.COLORMAP_JET)
cv2.imwrite(path + uv_image, uimage)

app = Flask(__name__)


wiki = wikipedia.summary(imgName, sentences:3)

def send_for_identificattion(file_name):
	files_encoded = []
	with open(file_name, 'rb') as file:
		files_encoded.append(base64.b64encode(file.read()).decode('ascii'))

	params = {
		'images': files_encoded,
		'key': secret_access_key,
		'parameters': ["crops_fast"]
	}
	headers = {
		'Content-Type': 'application/json'
	}

	response = requests.post('https://plant.id/api/identify', json=params, headers=headers)

	if response.status_code != 200:
	    raise("send_for_identificattion error: {}".format(response.text))

	return response.json().get('id')


def get_suggestions(request_id):
	params = {
	    "key": secret_access_key,
	    "ids": [request_id]
	}
	headers = {
	    'Content-Type': 'application/json'
	}

	while True:
		print("Waiting for suggestions...")
		sleep(5)
		resp = requests.post('https://plant.id/api/check_identifications', json=params, headers=headers).json()
		if resp[0]["suggestions"]:
			return resp[0]["suggestions"]

@app.route("/")
def index():
    # request_id = send_for_identificattion(img)
    # for suggestion in get_suggestions(request_id):
    #     imgName = (suggestion["plant"]["name"])
    return(render_template('plantInfo.html', img=reg_img, cb_img=cb_image, uv_img=uv_image, wiki=wiki, link=link, name=name))


if __name__ == "__main__":
    app.run(debug=True)
