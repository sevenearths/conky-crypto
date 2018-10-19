import os, sys, time, math, json, urllib
import pprint

millnames = ['','T','M','B','T']
millnamesfull = ['',' Thousand',' Million',' Billion',' Trillion']

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


filename = 'crypto_conky.txt'

base_url = 'https://api.coinmarketcap.com/v2/'

coinNames = [
	'ICX',
	'ETH',
	'EOS',
	'LTC',
	'XRP'
]

url = base_url + 'listings/'
response = urllib.urlopen(url)
coinsList = json.loads(response.read())
coins = {}
for coinName in coinNames:
	try:
		coinDetails = (item for item in coinsList["data"] if item["symbol"] == coinName).next()
		coins[coinName] = coinDetails["id"]
	except:
		pass

sorted(coins)

coins['BTC'] = 1

url = base_url + 'global/'
response = urllib.urlopen(url)
globalData = json.loads(response.read())

bp = round(float(globalData['data']['bitcoin_percentage_of_market_cap']), 2)
tmc = globalData['data']['quotes']['USD']['total_market_cap']
tv24h = globalData['data']['quotes']['USD']['total_volume_24h']
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

for coin, id in sorted(coins.items()):
	url = base_url + 'ticker/' + str(id)
	response = urllib.urlopen(url)
	jsonData = json.loads(response.read())

	if 'timestamp' not in coinData:
		coinData['timestamp'] = jsonData['metadata']['timestamp']

	cs    = jsonData['data']['circulating_supply']
	ts    = jsonData['data']['total_supply']
	price = jsonData['data']['quotes']['USD']['price']
	v24   = jsonData['data']['quotes']['USD']['volume_24h']
	mc    = jsonData['data']['quotes']['USD']['market_cap']
	mce   = round((float(cs)*float(price)), 0) if cs and price else -100.0
	pc1h  = jsonData['data']['quotes']['USD']['percent_change_1h']
	pc24h = jsonData['data']['quotes']['USD']['percent_change_24h']
	pc7d  = jsonData['data']['quotes']['USD']['percent_change_7d']

	coinData[coin] = {}
	coinData[coin]['rank']                   = int(jsonData['data']['rank'])
	coinData[coin]['percent_in_circulation'] = round((float(cs)/(int(ts)/100)), 2) if cs and ts else -100.0
	coinData[coin]['price']                  = round(float(price), 2)
	coinData[coin]['volume_24h']             = millify(v24) if v24 else 0.0
	coinData[coin]['market_cap']             = millify(mc) if mc else millify(mce)
	coinData[coin]['volume_as_percent']      = round((float(v24)/(int(mc)/100)), 2) if v24 and mc else -100.0
	coinData[coin]['percent_change_1h']      = float(pc1h) if pc1h else -100.0
	coinData[coin]['percent_change_24h']     = float(pc24h) if pc24h else -100.0
	coinData[coin]['percent_change_7d']      = float(pc7d) if pc7d else -100.0

	coinData[coin]['volume_as_percent_colour']  = 'red'
	coinData[coin]['percent_change_1h_colour']  = 'red'
	coinData[coin]['percent_change_24h_colour'] = 'red'
	coinData[coin]['percent_change_7d_colour']  = 'red'

	if coinData[coin]['volume_as_percent'] > 2.5:
		coinData[coin]['volume_as_percent_colour'] = 'orange'
	if coinData[coin]['volume_as_percent'] > 5.0:
		coinData[coin]['volume_as_percent_colour'] = 'green'

	if coinData[coin]['percent_change_1h'] > 0.0:
		coinData[coin]['percent_change_1h_colour'] = 'orange'
	if coinData[coin]['percent_change_1h'] > 20.0:
		coinData[coin]['percent_change_1h_colour'] = 'green'

	if coinData[coin]['percent_change_24h'] > 0.0:
		coinData[coin]['percent_change_24h_colour'] = 'orange'
	if coinData[coin]['percent_change_24h'] > 20.0:
		coinData[coin]['percent_change_24h_colour'] = 'green'

	if coinData[coin]['percent_change_7d'] > 0.0:
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
file.write("${font sans-serif:bold:size=10}Total Market Cap:${alignr}${color "+tmc_colour+"}"+millifyfull(globalData['data']['quotes']['USD']['total_market_cap'])+"${color}\n")
file.write("${font sans-serif:bold:size=2} \n")
file.write("${font sans-serif:bold:size=8}COIN${goto 50}MC${goto 90}Price${goto 120}Vol %${goto 165}1hr${goto 205}24hr${goto 245}7d\n")
file.write("${hr 1}\n")

for coin, id in sorted(coins.items()):
	if coin is not 'BTC':
		file.write('${font sans-serif:normal:size=8}'+str(coin)+': ${goto 50}'+str(coinData[coin]["market_cap"])+'${goto 90}'+str(coinData[coin]["price"])+'${goto 125}${color '+coinData[coin]["volume_as_percent_colour"]+'}'+str(coinData[coin]["volume_as_percent"])+'${goto 160}${color '+coinData[coin]["percent_change_1h_colour"]+'}'+str(coinData[coin]["percent_change_1h"])+'${goto 200}${color '+coinData[coin]["percent_change_24h_colour"]+'}'+str(coinData[coin]["percent_change_24h"])+'${goto 240}${color '+coinData[coin]["percent_change_7d_colour"]+'}'+str(coinData[coin]["percent_change_7d"])+'${color}\n')

file.close()