import os, sys, time, math, json, pprint, requests
from urllib2 import Request, urlopen
from urllib import urlencode

millnames = ['','T','M','B','T']
millnamesfull = ['',' Thousand',' Million',' Billion',' Trillion']

coins_filename = 'coins.json'
filename = 'crypto_conky.txt'

api_key = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'

base_url = 'https://pro-api.coinmarketcap.com/v1/'

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
    	int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.1f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def millifyfull(n):
    n = float(n)
    millidx = max(0,min(len(millnamesfull)-1,
    	int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.1f}{}'.format(n / 10**(3 * millidx), millnamesfull[millidx])

def getCoins():
	coinsList = json.loads(apiRequest('cryptocurrency/map'))
	for coinName in coinNames:
		try:
			coinDetails = (item for item in coinsList["data"] if item["symbol"] == coinName).next()
			coins[coinDetails["id"]] = coinName
		except:
			pass

	sorted(coins)

	file = open(coins_filename, 'w')
	file.write(json.dumps(coins, ensure_ascii=False))
	file.close()

	return coins

def apiRequest(url, args = None):
	headers = {'X-CMC_PRO_API_KEY': api_key}
	params = args
	r = requests.get(base_url + url, headers=headers, params=params)
	return r.json()

coinNames = [
    'ICX',
    'ETH',
    'EOS',
    'LTC',
    'NEO',
    'GRS',
    'VIA',
    'VTC',
    'RUP',
    'RUPX',
    #'XTL',
    'SMART',
    'XTZ',
    'RVN',
    'MAS',
    'DASH',
    'DIVI',
]

coins = {}

if os.path.isfile(coins_filename) is False:
	coins = getCoins()
else:
	if os.path.isfile(coins_filename):
		with open(coins_filename) as json_data:
			coins = json.load(json_data)
			if len(coins) != len(coinNames):
				coins = getCoins()

coins[1] = 'BTC'

globalData = apiRequest('global-metrics/quotes/latest')

bp = round(float(globalData['data']['btc_dominance']), 2)
tmc = globalData['data']['quote']['USD']['total_market_cap']
tv24h = globalData['data']['quote']['USD']['total_volume_24h']
tvp = round((float(tv24h) / (float(tmc)/100)), 2)

bp_colour = 'red'
if bp < 30.0:
	bp_colour = 'orange'
if bp < 20.0:
	bp_colour = 'green'

tmc_colour = 'red'
if int(tmc) > 500000000000:
	tmc_colour = 'orange'
if int(tmc) > 1000000000000:
	tmc_colour = 'green'

tvp_color = 'red'
if tvp > 10.0:
	tvp_color = 'orange'
if tvp > 20.0:
	tvp_color = 'green'

coinData = {}

ids = ','.join([str(x) for x in coins.keys()])
args = {'id':ids}

jsonData = apiRequest('cryptocurrency/quotes/latest', args)

for id, coin in sorted(coins.items()):

	if str(id) in jsonData['data']:

		coinInfo = jsonData['data'][str(id)]

		cs    = coinInfo['circulating_supply']
		ts    = coinInfo['total_supply']
		price = coinInfo['quote']['USD']['price']
		v24   = coinInfo['quote']['USD']['volume_24h']
		mc    = coinInfo['quote']['USD']['market_cap']
		mce   = round((float(cs)*float(price)), 0) if cs and price else -100.0
		pc1h  = coinInfo['quote']['USD']['percent_change_1h']
		pc24h = coinInfo['quote']['USD']['percent_change_24h']
		pc7d  = coinInfo['quote']['USD']['percent_change_7d']

		coinData[coin] = {}
		coinData[coin]['rank']                   = int(coinInfo['cmc_rank'])
		coinData[coin]['percent_in_circulation'] = round((float(cs)/(int(ts)/100)), 2) if cs and ts else -100.0
		coinData[coin]['price']                  = round(float(price), 2)
		coinData[coin]['volume_24h']             = millify(v24) if v24 else 0.0
		coinData[coin]['market_cap']             = millify(mc) if mc else millify(mce)
		coinData[coin]['volume_as_percent']      = round((float(v24)/(int(mc)/100)), 2) if v24 and mc else -100.0
		coinData[coin]['percent_change_1h']      = round(float(pc1h), 2) if pc1h else -100.0
		coinData[coin]['percent_change_24h']     = round(float(pc24h), 2) if pc24h else -100.0
		coinData[coin]['percent_change_7d']      = round(float(pc7d), 2) if pc7d else -100.0

		coinData[coin]['volume_as_percent_colour']  = 'red'
		coinData[coin]['percent_change_1h_colour']  = 'red'
		coinData[coin]['percent_change_24h_colour'] = 'red'
		coinData[coin]['percent_change_7d_colour']  = 'red'

		if coinData[coin]['volume_as_percent'] > 2.5:
			coinData[coin]['volume_as_percent_colour'] = 'orange'
		if coinData[coin]['volume_as_percent'] > 5.0:
			coinData[coin]['volume_as_percent_colour'] = 'green'

		if coinData[coin]['percent_change_1h'] > 2.0:
			coinData[coin]['percent_change_1h_colour'] = 'orange'
		if coinData[coin]['percent_change_1h'] > 20.0:
			coinData[coin]['percent_change_1h_colour'] = 'green'

		if coinData[coin]['percent_change_24h'] > 2.0:
			coinData[coin]['percent_change_24h_colour'] = 'orange'
		if coinData[coin]['percent_change_24h'] > 20.0:
			coinData[coin]['percent_change_24h_colour'] = 'green'

		if coinData[coin]['percent_change_7d'] > 2.0:
			coinData[coin]['percent_change_7d_colour'] = 'orange'
		if coinData[coin]['percent_change_7d'] > 20.0:
			coinData[coin]['percent_change_7d_colour'] = 'green'

file = open(filename, 'w')

btc_price = round(float(coinData['BTC']['price']),2)

btc_color = 'red'
if btc_price > 10000.0:
	btc_color = 'orange'
if btc_price > 20000.0:
	btc_color = 'green'

file.write("${font sans-serif:bold:size=11}CRYPTO ${hr 2}\n")
file.write("${font sans-serif:bold:size=10}Bitcoin Price:${alignr}${color "+btc_color+"}"+str(btc_price)+"${color}\n")
file.write("${font sans-serif:bold:size=10}Trading Volume:${alignr}${color "+tvp_color+"}"+str(tvp)+"%${color}\n")
file.write("${font sans-serif:bold:size=10}Bitcoin Market Share:${alignr}${color "+bp_colour+"}"+str(bp)+"%${color}\n")
file.write("${font sans-serif:bold:size=10}Total Market Cap:${alignr}${color "+tmc_colour+"}"+millifyfull(globalData['data']['quote']['USD']['total_market_cap'])+"${color}\n")

file.write("${font sans-serif:bold:size=2} \n")
file.write("${font sans-serif:bold:size=8}COIN${goto 50}MC${goto 90}Price${goto 120}Vol %${goto 165}1hr${goto 205}24hr${goto 245}7d\n")
file.write("${hr 1}\n")

# dict((y,x) for x,y in my_dict.iteritems())
for coin in sorted(dict((y,x) for x,y in coins.iteritems()).keys()):
	if coin is not 'BTC':
		file.write('${font sans-serif:normal:size=8}'+str(coin)+': ${goto 50}'+str(coinData[coin]["market_cap"])+'${goto 90}'+str(coinData[coin]["price"])+'${goto 125}${color '+coinData[coin]["volume_as_percent_colour"]+'}'+str(coinData[coin]["volume_as_percent"])+'${goto 160}${color '+coinData[coin]["percent_change_1h_colour"]+'}'+str(coinData[coin]["percent_change_1h"])+'${goto 200}${color '+coinData[coin]["percent_change_24h_colour"]+'}'+str(coinData[coin]["percent_change_24h"])+'${goto 240}${color '+coinData[coin]["percent_change_7d_colour"]+'}'+str(coinData[coin]["percent_change_7d"])+'${color}\n')

file.close()
