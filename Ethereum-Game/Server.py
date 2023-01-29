from flask import Flask, request, jsonify
import json
import Web3Interface, Validation

app = Flask(__name__)

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    x = data['x']
    y = data['y']
    print(x, y)
    if not Validation.Validate(data):
        print('[S] Signature is invalid.')
        return 'False'
    print('[YAY] Signature is valid. Player position updated.')
    if x == '1' or x == '-1':
        Web3Interface.GanacheContract('set_x', str(int(Web3Interface.GanacheContract('get_x', 0)) + int(x)))
        return 'True'
    elif y == '1' or y == '-1':
        Web3Interface.GanacheContract('set_y', str(int(Web3Interface.GanacheContract('get_y', 0)) + int(y)))
        return 'True'
    else:
        return 'False'
@app.route('/getPosition', methods=['GET'])
def getPosition():
    return str([Web3Interface.GanacheContract('get_x', 0), Web3Interface.GanacheContract('get_y', 0)])
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
