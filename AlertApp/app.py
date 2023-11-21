from flask import Flask,request, redirect, render_template
from alert import Alert, UseAlert, create_alert_json, create_alert_dict
import json
from multiprocessing import Process


app = Flask(__name__)
alert_thread = None

#utility functions 
#function to start alert in a thread
def start_alert(alertdict,):
	global alert_thread
	print("alert_started")
	l = len(alertdict.keys())
	print('alerts_for: ', alertdict)
	compleated = []
	while l>0:
		for price, alert in alertdict.items():
			if price not in compleated:
				
				lp = alert.lastprice()
				if ',' in lp:
					lp = lp.replace(',', '')
				lp = float(lp)
				if alert.type == 'ge':
					if lp >= alert.ap:
						alert.sendit()
						u = UseAlert('alerts.json')
						jo = u.view_json()
						jo.pop(str(alert.ap))
						u.change_json(jo)
						compleated.append(str(alert.ap))
						# return None
					else:
						# print(lp)
						pass
				elif alert.type == 'le':
					if lp <= alert.ap:
						alert.sendit()
						u = UseAlert('alerts.json')
						jo = u.view_json()
						jo.pop(str(alert.ap))
						u.change_json(jo)
						compleated.append(str(alert.ap))

						# return None
					else:
						# print(lp)
						pass

	alert_thread = None						
	print('alert_thread_end')


#utility function till here


#app routes from here on
#main route (index.html)
@app.route("/", methods=['POST', 'GET'])
def index():
	global alert_thread

	if request.method == 'POST':
		asset = request.form.get('asset').upper()
		ap = float(request.form.get('alertprice'))
		typ = request.form.get('oftype')

		u = UseAlert('alerts.json')
		v = u.view_json()
		v2 = create_alert_json(asset, ap, typ)
		v.update(v2)
		u.change_json(v)

		if alert_thread: 
			alert_thread.terminate()
			alert_thread = None
			return redirect('/startalert')
		else:
			return redirect('/alerts')



	return render_template("index.html", appname='alert_app')


#route to view alerts
@app.route('/alerts', methods=['POST', 'GET'])
def all_alerts():
	u = UseAlert('alerts.json')
	jo = u.view_json()

	return render_template('all_alerts.html',alert_details=jo,)



#route to delete alerts
@app.route('/delete/<alertprice>')
def delete_alert(alertprice):
	global alert_thread
	u = UseAlert('alerts.json')
	v = u.view_json()
	v.pop(str(alertprice))
	u.change_json(v)
	jo = u.view_json()
	if alert_thread:
		# print('here in delete if')
		alert_thread.terminate()
		alert_thread = None
		return redirect('/startalert')
	elif alert_thread == None:
		# print('here in delete else')
		return redirect('/alerts')

	return render_template('all_alerts.html',alert_details=jo,)



#route to start alerts
@app.route('/startalert')
def alert_start():
	global alert_thread
	u = UseAlert('alerts.json')
	jo = u.view_json()
	alertdct = create_alert_dict(jo)

	p = Process(target=start_alert, args=(alertdct,))
	p.start()
	alert_thread = p
	print('alert_started_with_thread: ', alert_thread)
	return redirect('/alerts')


#route to end alerts
@app.route('/endalert')
def alert_end():
	global alert_thread
	print(alert_thread, 'is current alerte thread')
	if alert_thread:
		alert_thread.terminate()
		print('_alert_ended_')
		alert_thread = None
	return redirect("/alerts")


#app routes till here


if __name__ == "__main__":
	app.run(debug=True, port=8000)