from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data['message']
    response = generate_response(message)
    return jsonify({'response': response})

def generate_response(message):
    apiKey = 'sk-...'
    endpoint = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {apiKey}'
    }
    payload = {
        'model': 'gpt-3.5-turbo-0125',
        'prompt': message,
        'max_tokens': 150  # Adjust as needed
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    data = response.json()
    print(data)
    return data['choices'][0]['text'].strip()



@app.route('/solve/<uuid>', methods=['GET', 'POST'])
def api_request(uuid):
    content = request.json
    table = content['table']
    solved = solve_sudoku(table)
    print("Returning the following solved Sudoku from the server:")
    print(is_valid_sudoku(solved))
    if solved is None:
        return jsonify({"uuid":uuid, 'message':'Sudoku cannot be solved'})
    return jsonify({"uuid":uuid, 'solved':solved})

def is_valid_sudoku(grid):
    for i in range(9):
        if len(set(grid[i])) != 9 or len(set([grid[j][i] for j in range(9)])) != 9:
            return False
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if len(set([grid[x][y] for x in range(i, i+3) for y in range(j, j+3)])) != 9:
                return False
    return True

def find_empty_location(arr):
    for row in range(9):
        for col in range(9):
            if arr[row][col] == 0:
                return row, col
    return -1, -1

def used_in_row(arr, row, num):
    return any(num == arr[row][col] for col in range(9))

def used_in_col(arr, col, num):
    return any(num == arr[row][col] for row in range(9))

def used_in_box(arr, row, col, num):
    for r in range(3):
        for c in range(3):
            if arr[r + row][c + col] == num:
                return True
    return False

def is_location_safe(arr, row, col, num):
    return not used_in_row(arr, row, num) and not used_in_col(arr, col, num) and not used_in_box(arr, row - row % 3, col - col % 3, num)

def solve_sudoku(arr):
    row, col = find_empty_location(arr)
    if row == -1 and col == -1:
        return arr

    for num in range(1, 10):
        if is_location_safe(arr, row, col, num):
            arr[row][col] = num
            if solve_sudoku(arr):
                return arr
            arr[row][col] = 0
    return None  # return None if the Sudoku can't be solved

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)