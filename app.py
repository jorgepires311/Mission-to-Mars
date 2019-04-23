from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/dbMars")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    marsData = mongo.db.dbMars.find_one()

    # Return template and data
    return render_template("index.html", marsData = marsData )


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    marsDb = mongo.db.dbMars
    # Run the scrape function
    marsData = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.dbMars.update({}, marsData, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
