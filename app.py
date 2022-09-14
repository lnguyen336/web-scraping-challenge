# Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask-pymongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home(): 

    # Find one record of data from the mongo database and return it
    mars_data = mongo.db.marsData.find_one()

    # Return template and data
    return render_template('index.html', mars = mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    nasa_table = mongo.db.marsData
    mongo.db.marsData.drop()

    # Call the scrape function in the scrape_mars file which will scrape and save to mongo
    mars_info = scrape_mars.scrape()

    # Update database with data being scraped
    nasa_table.update_one({}, {'$set': mars_info}, upsert = True)

    # Redirect back to home page and return a message to show it was succesful
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)