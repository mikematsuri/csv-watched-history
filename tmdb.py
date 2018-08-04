# Short script to use tmdbsimple to input list of titles and parse their TMDB ID

# This product uses the TMDb API but is not endorsed or certified by TMDb.

from time import sleep

import tmdbsimple as tmdb
tmdb.API_KEY = "YOUR_API_KEY_HERE"

out = open('output.txt', 'w')
f = open('titles.txt', 'r')

for row in f:
    search = tmdb.Search()
    response = search.movie(query=row.strip())
    
    if len(search.results) == 0:
        print("Unable to locate result for: " + row.strip())
        out.write("0000000000" + "\n")
    else:
        out.write(str(search.results[0]['id']) + "\n")
    
    # Sleep to prevent going over request limit of 40 per 10 seconds
    sleep(.3)

out.close()
f.close()