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
    API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNDMxNTk5NzEtOTRiNC00NjIxLTgwMDEtNWZhNDc1NDUwNmYyIiwidHlwZSI6ImFwaV90b2tlbiJ9.TmaYrVHsHgq9dYqD7t-yQba8aaX0XKu-VNaLWGgbPzE'
    question = message
    url = f"https://api.edenai.co/v1/question-answering"
    headers = {
        f'Authorization':'Bearer 🔑 {API_KEY}'
    }
    data = {
        "question": question
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        data = response.json()
        answer = data.get('answer')
        return f"Answer: {answer}"
    else:
        print(f"Error: {response.status_code}")
        print(response.text)



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