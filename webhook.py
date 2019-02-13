import json
import os
import requests
import datetime


from flask import Flask
from flask import request
from flask import make_response

#Flask app should start in global layout
app = Flask(__name__)




@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  #print(json.dumps(req, indent=4))

  res = makeResponseone(req)
  res = json.dumps(res, indent=4)
  #print(res)
  r = make_response(res)
  r.headers['Content-Type'] = 'application/json'
  return r





def makeResponseone(req):
  result = req.get("queryResult")
  parameters = result.get("parameters")
  city= parameters.get("geo-city")
  date= parameters.get("date")

  da=date.strftime(%y-%m-%d)
  print (da)

  r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=d3720b72a53ba44d5740632909d372a1')    
  json_object = r.json()
  weather=json_object['list']
  #print(json.dumps(weather, indent =4))
  condition ="sunny"
  for i in range(0,30):
    #print (weather[i]['dt_txt'])
    #print (date)
    if date in weather[i]['dt_txt']:
       condition= weather[i]['weather'][0]['description']
       print (condition)
       print (date)
       break


  resp = "The forecast in "+city+" for "+date+" is " +condition

  return {
      "fulfillmentText": resp
      #"text": resp
         #"source": "Dialogflow-weather-webhook"
    }





if __name__ == '__main__':
     port = int(os.getenv('PORT', 5000))
     print("Starting app on port %d" % port)
     app.run(debug=False, port=port, host='0.0.0.0')

