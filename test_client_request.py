import requests as re

url = input('Entrer l\'url du site :')

while True:
    response = re.get(url)
    print(response.status_code)