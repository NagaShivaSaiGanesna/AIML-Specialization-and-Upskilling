from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to this Flask course! This is the home page."

if __name__ == "__main__":
    app.run(debug=True)