from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/login",methods = ['POST', 'GET'])
def hello_world():
   return "hi"

if __name__ == "__main__":
    app.run()

