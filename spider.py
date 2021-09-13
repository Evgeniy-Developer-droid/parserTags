import requests
import time 
import json
import pickle
import os

def twitter():
	headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAABLURwEAAAAAHxdfh34yHeo4QJwPwj8hERELUgg%3D4RYi2ioeBB0dgWLsEzyfGgYyVTLwhKQGKh9pSWMyPRQGHtAcxT"}
	with open("data.json", "r") as jsonFile:
		jsonObject = json.load(jsonFile)
		for hash_name in jsonObject['hashtags']:
			response = requests.get("https://api.twitter.com/2/tweets/counts/recent?query="+hash_name.split("#")[1], headers=headers).json()
			# return hash_name.split("#")[1]
			if len(jsonObject['data']['twitter']) != 0:
				finded = False
				for obj in jsonObject['data']['twitter']:
					if hash_name in obj:
						obj[hash_name] = int(obj[hash_name]) + (int(response['meta']['total_tweet_count']) - int(obj[hash_name]))
						finded = True
						break
				if not finded:
					jsonObject['data']['twitter'].append({hash_name:response['meta']['total_tweet_count']})
			else:
				jsonObject['data']['twitter'].append({hash_name: response['meta']['total_tweet_count']})
		jsonFile.close()
	jsonString = json.dumps(jsonObject)
	with open("data.json", "w") as file:
		file.write(jsonString)
		file.close()




def parser():
	try:
		with open("file_access.json", "r") as jsonFile1:
			accessObject = json.load(jsonFile1)
			jsonFile1.close()
		with open("data.json", "r") as jsonFile:
			jsonObject = json.load(jsonFile)
			jsonObject["data"]["instagram"] = []
			for hash_name in jsonObject['hashtags']:
				headers = {
					"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
					"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
					"cookie": "sessionid="+accessObject['instagram']['session_id']
				}
				response = requests.get("https://www.instagram.com/explore/tags/"+hash_name.split("#")[1]+"/?__a=1", headers=headers)
				hashtag = json.loads(response.text)["data"]["media_count"]
				jsonObject["data"]["instagram"].append({hash_name:hashtag})
				jsonString = json.dumps(jsonObject)
				time.sleep(3)
			jsonFile.close()
		with open("data.json", "w") as file:
			file.write(jsonString)
			file.close()
	finally:
		pass

