from flask import Flask, jsonify

print 'starting app'
app = Flask(__name__)


@app.route('/movies')
def api_root():
    return jsonify(["Matt and Deans amazing adventures",
    "Why did Jenny fall asleep", "Pulp Fiction"])
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False)
