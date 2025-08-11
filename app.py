from flask import Flask, render_template, request
from knowledge_base import get_feed_recommendation

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        chicken_type = request.form.get("chicken_type")
        age_days = int(request.form.get("age_days"))

        recommendation = get_feed_recommendation(chicken_type, age_days)
        return render_template("result.html", recommendation=recommendation, chicken_type=chicken_type, age_days=age_days)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
