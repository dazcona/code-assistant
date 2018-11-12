import requests
import random

url = 'https://api.github.com/users/dazcona/gists'

'''TODO
1. Use pagination to get more than 30 gists
2. Don't repeat gists (use db)

'''
def gist():

    resp = requests.get(url=url)
    data = resp.json()
    total_gists = len(data)
    r_index = random.randint(0,total_gists)
    item = data[r_index]
    return item['html_url'], item['description']
