# This script is a modified form of tuxity's betaseries-to-trakt script, found at
# https://github.com/tuxity/betaseries-to-trakt
#
# The following implementation is meant to work with custom data (not from Betaseries)
# and also add specific watch dates for history of movies

import csv
import json
import os
import re
import requests
import sys

# User must run script after configuring the following fields
# PIN can be retrieved at below URI, replacing ________ with individual Client ID from an API application
# https://trakt.tv/oauth/authorize?response_type=code&client_id=________&redirect_uri=urn:ietf:wg:oauth:2.0:oob

clientid = ""
clientsecret = ""
onetimepin = ""

# First setup headers with identity and authorization

session = requests.Session()

session.headers.update({
    "Accept":     "application/json",
    "User-Agent": "CSV Watched History",
    "Connection": "Keep-Alive"
})

post_data = {
    "code":          onetimepin,
    "client_id":     clientid,
    "client_secret": clientsecret,
    "redirect_uri":  "urn:ietf:wg:oauth:2.0:oob", # ???
    "grant_type":    "authorization_code"
}

# Can comment out after first request, when access token has been granted
request = session.post("https://api.trakt.tv/oauth/token", data=post_data)
response = request.json()
print("Access token: " + response["access_token"])

session.headers.update({
    "Content-Type":      "application/json",
    "trakt-api-version": "2",
    "trakt-api-key":     clientid,
    "Authorization":     "Bearer " + response["access_token"] # Replace with access token for multiple requests
})

# Construct a dictionary to hold an array of movie objects, populated from the imported csv

historydata = {
        "movies": []
    }

f = open("imp.csv", "r")
c = csv.reader(f)
for row in c:
    movie = {
        "watched_at": row[1],
        "title": row[0],
        "ids": {
            "tmdb": int(row[2])
        }
    }
    historydata["movies"].append(movie)

f.close()

# Output post data and response for confirmation in case of issue. Then send HTTP POST and check if success.
print("Movies to be added:")
print(historydata)
request_history = session.post("https://api.trakt.tv/sync/history", data=json.dumps(historydata))
print("Server response: " + request_history.text)
response_history = request_history.json()

if int(request_history.status_code) == 500:
    print("HTTP 500 error. Exiting")
else:
    print("Script done. Added " + str(response_history['added']['movies']) + " movies.")