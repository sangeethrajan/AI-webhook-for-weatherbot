import json
import os
import requests
import datetime


from flask import Flask
from flask import request
from flask import make_response
from datetime import datetime

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
  
  #2019-02-14T12:00:00-05:00
  #datetimedialog_object = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S-%H:%M')
  #print (datetimeweather_object.date())

  #da=date.strftime("%m/%d/%Y, %H:%M:%S")
  #print (da)

  r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=d3720b72a53ba44d5740632909d372a1')    
  json_object = r.json()
  weather=json_object['list']
  #print(json.dumps(weather, indent =4))
  condition ="sunny"
  for i in range(0,30):
    #print (weather[i]['dt_txt'])
    #print (date)
    #2019-02-14 00:00:00
    #datetimeweather_object = datetime.strptime(weather[i]['dt_txt'], '%Y-%m-%d %H:%M:%S')
    #print (datetimeweather_object.date())
    if date in weather[i]['dt_txt']:
    #if datetimedialog_object.date() == datetimeweather_object.date():
       condition= weather[i]['weather'][0]['description']
       #print (condition)
       #print (date)
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

