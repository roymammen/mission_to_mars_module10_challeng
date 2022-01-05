from flask import Flask, render_template, redirect
import pymongo
# from flask_pymongo import PyMongo
import scraping

# Create an instance of Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
conn = "mongodb://localhost:27017"
try:
    # client = pymongo.MongoClient(
    #     host = "localhost",
    #     port = 27017,
    #     serverSelecionTimeoutMS = 1000
    # )
    client = pymongo.MongoClient(conn)
    db = client.local 
    client.server_info() # trigger exception if not connected to db!


except:
    print("ERROR - Cannot connect to db")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find all record of data from the mongo database
    mars_dict = db.mars_dict.find({})
    # mars_data = scraping.scrape_all()
    # Update the Mongo database using update and upsert=True    
    # db.mars_dict.insertMany(mars_data)
    # Return template and data
    return render_template("index.html", mars=mars_dict)


@app.route("/scrape")
def scrape():
  
    # mars_dict = db.mars_dict.find({})
    mars_data = scraping.scrape_all()
    # Update the Mongo database using update and upsert=True    
    db.mars_dict.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    # If running as script, print scraped data
    app.run(debug=True)
