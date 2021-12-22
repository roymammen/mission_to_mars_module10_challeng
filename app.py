from flask import Flask, render_template, redirect
import pymongo
# from flask_pymongo import PyMongo
import scraping

# Create an instance of Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.local 

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_dict = db.mars_dict.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict["img_url"])


@app.route("/scrape")
def scrape():
  
    mars_dict = db.mars_dict.find({})
    mars_data = scraping.scrape_all()
    # Update the Mongo database using update and upsert=True    
    mars_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    # If running as script, print scraped data
    app.run(debug=True)