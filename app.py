from flask import Flask, render_template, request, redirect, url_for
import requests as request2
import app_config
import json

app = Flask(__name__)
app.config.from_object(app_config)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def home(): 
 response = request2.get(app.config["REQUEST_URL"] + 'getNotes')
 notes = response.json()
 return render_template("index.html", notes=notes)

@app.route('/create', methods=("GET","POST"))
def create():
  try:
    if request.method=='POST':     
      id=request.form['id']
      title=request.form['title']
      author=request.form['author']

      if not id:
        flash("id is required!")
      elif not author:
        flash("author is required")
      elif not title:
        flash("title is required")
      else: 
        #payload="{\r\n    \"id\":\"1234\",\r\n    \"title\": \"none\",\r\n    \"author\": \"anonymous\"\r\n}"  
        json_object=json.dumps({'id':id,'title':title,'author':author})
        headers = {
          'Content-Type': 'application/json'
        }
        response = request2.request("POST",
                                    url=app.config["REQUEST_URL"] + 'createNote',                                                               
                                    data=json_object)  
        
        return redirect(url_for('home'))
    else:
      return render_template("create.html")       
  except Exception as e:
    app.logger.error(str(e))
    return render_template("error.html",data=str(e))
 
