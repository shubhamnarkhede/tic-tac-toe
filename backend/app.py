from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# creating sqlite temporary DB instance
def init_db():
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS board (cell_index INTEGER PRIMARY KEY, value TEXT)') # Create the Board table
    conn.commit()
    conn.close()

# Logic of winning cases
def check_winner(board):
    winning_combos = [
        [0,1,2], [3,4,5], [6,7,8],  
        [0,3,6], [1,4,7], [2,5,8],  
        [0,4,8], [2,4,6]            
    ]

    for combo in winning_combos:
        a, b, c = combo
        if board[a] != '' and board[a] == board[b] == board[c]:
            return board[a]
    if '' not in board:
        return 'draw'
    return None

# Api endpoint to get Update from frontend 
@app.route('/update', methods=['POST'])
def update_board():

    data = request.get_json()
    board = data.get('board')

    conn = sqlite3.connect('game.db') #Connecting to the DB
    c = conn.cursor()
    c.execute('DELETE FROM board') # Delete From Board 
    for i, val in enumerate(board):
        c.execute('INSERT INTO board (cell_index, value) VALUES (?, ?)', (i, val))  #insert the udpated matrix value according to which user clicked on the given cell
    conn.commit()
    conn.close()

    result = check_winner(board) # on each udpate check if there is any winner
    return jsonify({'status': result if result else 'continue'})
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
