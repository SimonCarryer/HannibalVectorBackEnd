from flask import Flask, jsonify

print 'starting app'
app = Flask(__name__)


@app.route('/movies')
def api_root():
    return jsonify(["Matt and Deans amazing adventures",
    "Why did Jenny fall asleep", "Pulp Fiction"])

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
