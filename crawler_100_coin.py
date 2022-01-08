from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import xlsxwriter

try:
  parameters = {
  'start':'1',
  'limit':'100',
  'sort': 'cmc_rank'
  }

  headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'c5d5dc31-64d6-44ed-813b-d7869f2dbb0a',
  } 

  session = Session()
  session.headers.update(headers)

  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
  response = session.get(url, params=parameters)

  data = response.json()
  row = 0

  workbook = xlsxwriter.Workbook('report_top_100_coin.xlsx')
  worksheet = workbook.add_worksheet("sheet1")
  worksheet.write(row, 1, 'name')
  worksheet.write(row, 2, 'time')
  worksheet.write(row, 3, 'open')
  worksheet.write(row, 4, 'high')
  worksheet.write(row, 5, 'low')
  worksheet.write(row, 6, 'close')
  worksheet.write(row, 7, 'volume')
  worksheet.write(row, 8, 'marketCap')

  row = row + 1
  index = 1

  for d in response.json()['data']:
      print(d['id'], d['name'], d['symbol'])
      param = {
          'id': d['id'],
          'range': '1Y',
          'convertId': '2781',
          'timeStart': '1609459200',
          'timeEnd': '1640995200'
      }

      resp = session.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical', params=param)

      for t in resp.json()['data']['quotes']:
          col = 1
          worksheet.write(row, col, d['symbol'])
          col = col + 1          
          worksheet.write(row, col, t['timeOpen'])
          col = col + 1
          worksheet.write(row, col, t['quote']['open'])
          col = col + 1
          worksheet.write(row, col, t['quote']['high'])
          col = col + 1
          worksheet.write(row, col, t['quote']['low'])
          col = col + 1
          worksheet.write(row, col, t['quote']['close'])
          col = col + 1
          worksheet.write(row, col, t['quote']['volume'])
          col = col + 1
          worksheet.write(row, col, t['quote']['marketCap'])
          col = col + 1
          worksheet.write(row, col, index)
          row = row + 1

      index = index + 1

  workbook.close()
 
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)