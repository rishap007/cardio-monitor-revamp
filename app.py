from flask import Flask, render_template, request

import prediction


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods=["POST"])
def predict():
    fields = (
        "age", "sex", "cp", "trestbps", "restecg", "chol", "fbs",
        "thalach", "exang", "oldpeak", "slope", "ca", "thal",
    )
    values = {field: request.form.get(field, "") for field in fields}
    try:
        result = prediction.preprocess(**values)
    except ValueError as error:
        return render_template("error.html", message=str(error)), 400

    patient_name = request.form.get("name", "").strip() or "there"
    return render_template(
        "result.html", prediction=result, nameofpatient=patient_name,
    )


@app.route("/about")
def about():
    return render_template("disease.html")


@app.errorhandler(500)
def internal_error(error):
    return render_template("error.html", message="Something went wrong. Please try again."), 500


@app.errorhandler(404)
def not_found(error):
    return "404 error", 404


if __name__ == "__main__":
    app.run(debug=False)
