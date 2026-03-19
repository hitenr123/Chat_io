import os

port = int(os.environ.get("PORT", 5000))

@app.route("/")
def home():
    return render_template("../templates/index.html")

app.run(host="0.0.0.0", port=port)