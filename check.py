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
# For unicode
reload(sys)
sys.setdefaultencoding('utf8')

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

# Construct the get URI as https://api.trakt.tv/users/_________/history/movies? with username in the gap
# include limit=4000 (or appropriate number), along with start_at and end_at to bound the results
attempt = session.get("")
that = attempt.content
data = json.loads(that)
myfile = open("check.csv", "w")
mytry = csv.writer(myfile, delimiter="\t")

i = 0
while i < len(data):
    mytry.writerow([str(data[i]["movie"]["title"]), str(data[i]["movie"]["year"]), str(data[i]["watched_at"])])
    i += 1

myfile.close()
