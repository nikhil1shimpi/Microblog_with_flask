import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
import urllib
import os
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv('MONGODB_URI'))
    app.db = client.microblog
    # entries = []

    @app.route('/', methods=['GET', 'POST'])
    def home():
        print([e for e in app.db.entries.find({})])
        if request.method == 'POST':
            entry_content = request.form.get("content")
            formated_date = datetime.datetime.today().strftime("%Y-%m-%d")
            # print(entry_content, formated_date)
            # entries.append((entry_content, formated_date))
            app.db.entries.insert_one({"content":entry_content, "date":formated_date})
        entries_with_date = [
            (entry["content"], 
            entry["date"], 
            datetime.datetime.strptime(entry["date"], '%Y-%m-%d').strftime("%b %d")) for entry in app.db.entries.find({})
        ]
        return render_template('home.html', entries=entries_with_date)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)     



