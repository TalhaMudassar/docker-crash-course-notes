from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    table_data = None
    number = None
    
    if request.method == "POST":
        try:
            # Get the number from the form
            number = int(request.form.get("number"))
            # Generate the multiplication table (1 to 10)
            table_data = [(number, i, number * i) for i in range(1, 11)]
        except ValueError:
            pass # Ignore invalid inputs for this simple app

    return render_template("index.html", number=number, table=table_data)

if __name__ == "__main__":
    # host="0.0.0.0" is REQUIRED for Docker to map the ports to your Windows machine!
    app.run(host="0.0.0.0", port=5000)