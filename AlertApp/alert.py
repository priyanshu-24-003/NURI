import nsepy
import requests
import json


# url = f"https://api.telegram.org/bot{token}/deleteMessage?chat_id={chat_id}&message_id={4}"
# url = f"https://api.telegram.org/bot{token}/getUpdates"


class Alert():

	def __init__(self, asset, alert_price, oftype):
		self.asset = asset
		if ',' in str(alert_price):
			alert_price.remove(',')
		self.ap = alert_price
		self.type = oftype

	def details(self,):
		return f'alert when price {self.type} to {self.ap} for {self.asset}'

	def lastprice(self,):

		q = nsepy.live.get_quote(self.asset)
		lp = q['data'][0]['lastPrice']
		return lp

	def sendit(self,):
		msg = f'price*Alert at {self.ap} for {self.asset}'

		token = "YOUR_UNIQUE_TOKEN"
		chat_id = "YOUR_UNIQUE_CHAT_ID"
		url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
		requests.get(url).json()
		return msg


class UseAlert():

	def __init__(self, filename):
		self.file = filename


	def change_json(self, newjsondict):
		with open(self.file, 'w') as f:
			json.dump(newjsondict, f)

	def view_json(self,):
		with open(self.file, 'r') as f:
			json_object = json.load(f)
		return json_object



def create_alert_json(asset, alert_price, oftyp):

	dct = {
		str(alert_price):{
			'asset':asset,
			'alert_price':alert_price,
			'oftype':oftyp
		}
	}
	return dct

def create_alert_dict(jsondict):
	dct = {}
	for price, alert in jsondict.items():
		if price != "price":
			a = Alert(alert['asset'], alert['alert_price'], alert['oftype'])
			dct[str(price)] = a

	return dct





if __name__ == '__main__':

		c = Alert('ITC', 330, 'ge')
		b = Alert('ICICIBank', 929, 'le')

		print(b.lastprice())






