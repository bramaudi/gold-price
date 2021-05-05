import requests, json
from http.server import BaseHTTPRequestHandler
from cowpy import cow
from bs4 import BeautifulSoup
from sanic import Sanic
from sanic.response import json

http = requests.get('https://harga-emas.org/')
soup = BeautifulSoup(http.content, 'html.parser')

def sort_type(kurs):
  return {
    "oz": kurs[0],
    "gr": kurs[1],
    "kg": kurs[2],
  }

list_usd = []
list_kurs_dollar = []
list_idr = []

table = soup.find_all('table')[1]
for tr in table.find_all('tr'):
  satuan = tr.select('td[align=left]')
  if len(satuan):
    # print(satuan[0].parent.find_all('td')[0]) # satuan
    usd = satuan[0].parent.find_all('td')[1]
    list_usd.append(usd.get_text())

    kurs_dollar = satuan[0].parent.find_all('td')[2]
    list_kurs_dollar.append(kurs_dollar.get_text())

    idr = satuan[0].parent.find_all('td')[3]
    list_idr.append(idr.get_text())

response = {
  'usd': sort_type(list_usd),
  'kurs_dollar': sort_type(list_kurs_dollar),
  'idr': sort_type(list_idr),
}

app = Sanic()

@app.route('/')
@app.route('/<path:path>')
async def index(request, path=""):
  return json(
    response,
    headers={"Access-Control-Allow-Origin": "*"}
  )

# app.run(host='0.0.0.0', port=8080)