from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/home")
def HomePage():
    return render_template("HomePage.html")  # Renders templates/index.html

@app.route("/static/ResourcePage.html")
def ResourcePage():
    return render_template("ResourcePage.html")

@app.route('/talk-to-ai', methods=['POST'])
def talk_to_ai():
    print("Mic button was clicked")
    # Replace this with AI handling logic
    return redirect(url_for('/static/HomePage.html'))  # or render_template(...)


if __name__ == "__main__":
    app.run(debug=True)
