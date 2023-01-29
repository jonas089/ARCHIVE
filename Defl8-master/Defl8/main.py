from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def website():
    return render_template('site.html')
@app.route('/agreement')
def agreement():
    return render_template('agreement.html')

app.run(host='127.0.0.1', port=80, debug=True)
#app.run(host='217.160.63.112', port=443) #HTTPS
#app.run(host='217.160.63.112', port=80) #HTTP
