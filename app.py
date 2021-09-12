# importing the necessary dependencies
import pandas as pd
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
from sklearn.preprocessing import StandardScaler

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/profile_report',methods=['GET'])  #view profile report
def viewProfileReport():
    return  render_template("profiling.html")

@app.route('/predict',methods=['POST']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            process_temp=float(request.form['process_temp'])
            rotational_speed = float(request.form['rotational_speed'])
            torque = float(request.form['torque'])
            tool_wear = float(request.form['tool_wear'])
            is_twf = request.form['twf']
            if(is_twf=='yes'):
                twf=1
            else:
                twf=0
            is_heat_dissipation =(request.form['heat_dissipation'])
            if(is_heat_dissipation =='yes'):
                heat_dissipation =1
            else:
                heat_dissipation =0
            is_power_failure = (request.form['power_failure'])
            if (is_power_failure == 'yes'):
                power_failure = 1
            else:
                power_failure = 0
            is_Overstrain_failure = (request.form['Overstrain_failure'])
            if (is_Overstrain_failure == 'yes'):
                Overstrain_failure = 1
            else:
                Overstrain_failure = 0
            is_Random_failure = (request.form['Random_failure'])
            if (is_Random_failure == 'yes'):
                Random_failure = 1
            else:
                Random_failure = 0

            filename = 'Predictive_Maintenance_model.pickle'
            data = pd.read_csv("data/ai4i2020.csv")
            x = data[['Process temperature [K]', 'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]', 'TWF', 'HDF',
                    'PWF', 'OSF', 'RNF']]
            scaler =  StandardScaler()
            x=scaler.fit_transform(x)
           # predictions using the loaded model file
            model = pickle.load(open('Predictive_Maintenance_model.pickle', 'rb'))
            prediction=model.predict(scaler.transform([[process_temp,rotational_speed,torque,tool_wear,twf,heat_dissipation,power_failure,Overstrain_failure,Random_failure]]))

            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=round(prediction[0]))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app