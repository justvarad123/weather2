from flask import Flask,request,make_response,render_template
import os,json
import requests


app = Flask(__name__)
#geting and sending response to dialogflow

@app.route('/weather-details', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("city")
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "c7258453da79906d58e0cf0e26e1ab7a"
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    # HTTP request
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
        # getting data in the json format
        list_of_data = response.json()
        report = list_of_data['weather']
        # data for variable list_of_data
        temp= list_of_data['main']['temp']- 273.15
        wt="Nice weather"
        tempe=float("{0:.2f}".format(temp)) 
        pressure=list_of_data['main']['pressure'] 
        humidity=list_of_data['main']['humidity']
        rep=report[0]['description']
        data="Today's weather in " + city + ": \n" + "Temperature in Celsius:" + tempe + "\n Pressure:" + pressure + "\n Humidity:" + humidity + "\n Weather Report:" + rep
        return {
        "fulfillmentText": data
        
        }
    else:
        return {
        "fulfillmentText": wt }
        
     
    
if __name__ == '__main__': 
    app.run(debug = True) 
