from flask import Flask, render_template, request
import pickle
import numpy as np
filename = 'HousePricePredictor.pkl'
model = pickle.load(open(filename, "rb"))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods = ["POST"])
def predict():
    temp_array = list()
    
    bedrooms = int(request.form["bedrooms"])
    bathrooms = int(request.form["bathrooms"])
    sqft_living = float(request.form["sqft_living"])
    sqft_lot = float(request.form["sqft_lot"])

    waterfront = request.form["waterfront"]
    if waterfront == 'Yes':
        waterfront = 1
        #temp_array = temp_array + [1]
    elif waterfront == "No":
        waterfront = 0
       #temp_array = temp_array + [0]

    sqft_above = float(request.form["sqft_above"])
    sqft_basement = float(request.form["sqft_basement"])
    temp_array = temp_array + [bedrooms, bathrooms, sqft_living, sqft_lot, waterfront, sqft_above, sqft_basement]

    condition = request.form["condition"]
    if condition == "best":
        #condition = 5
        temp_array = temp_array + [0,0,0,0,1]
    elif condition == "better":
       # condition = 4
        temp_array = temp_array + [0,0,0,1,0]
    elif condition == "good":
       # condition = 3
        temp_array = temp_array + [0,0,1,0,0]
    elif condition == "bad":
        #condition = 2
        temp_array = temp_array + [0,1,0,0,0]
    elif condition == "worse":
        #condition = 1
        temp_array = temp_array + [1,0,0,0,0]

    

    #waterfront = int(waterfront)
    #condition = int(condition)

    
    data = np.array([temp_array])
    
    pred = model.predict(data)
    output = round(pred[0], 2)

    return render_template("index.html", prediction_text = "Estimated house price is {} $".format(output))






if __name__ == "__main__":
    app.run(debug=True)

