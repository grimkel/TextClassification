from flask import Flask, render_template

app = Flask(__name__)

@app.route("/predict",  methods=['POST'])
def predict():
    pass

@app.route("/")
def mainpage():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()