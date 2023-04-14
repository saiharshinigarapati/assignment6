from flask import Flask, jsonify, request, render_template
import time

app = Flask(__name__)

class Game:
    def __init__(self, num_stones):
        self.num_stones = num_stones
        self.max_pickup = num_stones // 2
        self.piles = [num_stones, num_stones, num_stones]
        self.current_player = 1
        self.player_scores = [0, 0]
        self.round_start_time = 0

    def is_valid_move(self, pile_index, num_stones):
        if pile_index < 0 or pile_index > 2:
            return False
        if num_stones < 1 or num_stones > self.max_pickup:
            return False
        if num_stones > self.piles[pile_index]:
            return False
        return True

    def make_move(self, pile_index, num_stones):
        if self.is_valid_move(pile_index, num_stones):
            self.piles[pile_index] -= num_stones
            self.player_scores[self.current_player - 1] += num_stones
            self.current_player = 3 - self.current_player
            return True
        return False

    def get_game_state(self):
        return {
            "piles": self.piles,
            "current_player": self.current_player,
            "player_scores": self.player_scores,
            "max_pickup": self.max_pickup,
            "round_start_time": self.round_start_time
        }

    def start_round(self):
        self.round_start_time = time.time()

    def end_round(self):
        round_duration = time.time() - self.round_start_time
        return round_duration

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    num_stones = int(request.form['num_stones'])
    game = Game(num_stones)
    game.start_round()
    return render_template('game.html', game_state=game.get_game_state())

@app.route('/make_move', methods=['POST'])
def make_move():
    game_data = request.form
    game = Game(int(game_data['num_stones']))
    game.piles = [int(game_data[f'pile{i+1}']) for i in range(3)]
    game.player_scores = [int(game_data[f'score{i+1}']) for i in range(2)]
    game.current_player = int(game_data['current_player'])
    game.max_pickup = int(game_data['max_pickup'])
    pile_index = int(game_data['pile_index'])
    num_stones = int(game_data['num_stones'])
    if game.make_move(pile_index, num_stones):
        game.start_round()
        return render_template('game.html', game_state=game.get_game_state())
    return jsonify({'error': 'Invalid move'})

@app.route('/end_round', methods=['POST'])
def end_round():
    game_data = request.form
    game = Game(int(game_data['num_stones']))
    game.piles = [int(game_data[f'pile{i+1}']) for i in range(3)]
    game.player_scores = [int(game_data[f'score{i+1}']) for i in range(2)]
    game.current_player = int(game_data['current_player'])
    game.max_pickup = int(game_data['max_pickup'])
    round_duration = game.end_round()
    return render_template('round_end.html', round_duration=round_duration)


if __name__ == '__main__':
    app.run(debug=True)
