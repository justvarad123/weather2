from flask import Flask,request,make_response,render_template
import os,json
import requests

app = Flask(__name__) 

@app.route('/weather', methods =['POST', 'GET'])
def weather():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
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
        list_of_data = response.json()
        report = list_of_data['weather']
        # data for variable list_of_data
        temp= list_of_data['main']['temp']- 273.15
        wt="Nice weather"
        tempe=float("{0:.2f}".format(temp))
        pressure=list_of_data['main']['pressure']
        humidity=list_of_data['main']['humidity']
        rep=report[0]['description']
        data="Today's Weather in " + city + ": " + "Temperature: " + str(tempe) + " Celsius."+ " Pressure: " + str(pressure) +"." + " Humidity: " + str(humidity) +"." + " Weather Report: " + rep
    return {
            "fulfillmentText": data
        }

if __name__ == '__main__':
    app.run(debug = True) 
