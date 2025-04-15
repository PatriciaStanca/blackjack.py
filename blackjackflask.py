from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'secret_key'

# Kortvärden och färger
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['hearts', 'diamonds', 'clubs', 'spades']

face_cards = {
    'J': 'jack',
    'Q': 'queen',
    'K': 'king',
    'A': 'ace'
}

card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10,
    'jack': 10, 'queen': 10, 'king': 10, 'ace': 11
}

def deal_card():
    value = random.choice(values)
    suit = random.choice(suits)
    if value in face_cards:
        value = face_cards[value]
    return f"{value}_of_{suit}"

def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        value = card.split('_')[0]
        if value in face_cards:
            value = face_cards[value]
        score += card_values[value]
        if value == 'ace':
            aces += 1
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def compare(player_score, computer_score):
    if player_score > 21:
        return "You went over. You lose!"
    elif computer_score > 21:
        return "Computer went over. You win!"
    elif player_score > computer_score:
        return "You win!"
    elif computer_score > player_score:
        return "Computer wins!"
    else:
        return "It's a draw!"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'player_hand' not in session:
        session['player_hand'] = [deal_card(), deal_card()]
        session['computer_hand'] = [deal_card(), deal_card()]

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'hit':
            session['player_hand'].append(deal_card())
            session.modified = True
        elif action == 'stand':
            session['final_player_hand'] = session['player_hand'].copy()
            session.modified = True
            return redirect(url_for('result'))

    player_hand = session.get('player_hand', [])
    player_score = calculate_score(player_hand)

    return render_template('start.html', player_hand=player_hand, player_score=player_score)

@app.route('/result')
def result():
    player_hand = session.get('final_player_hand', [])
    computer_hand = session.get('computer_hand', [])

    player_score = calculate_score(player_hand)
    computer_score = calculate_score(computer_hand)

    while computer_score < 17:
        computer_hand.append(deal_card())
        computer_score = calculate_score(computer_hand)

    result_message = compare(player_score, computer_score)

    return render_template('result.html',
                           result=result_message,
                           player_hand=player_hand,
                           player_score=player_score,
                           computer_hand=computer_hand,
                           computer_score=computer_score)

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))

# Jinja2-filter för att generera bildväg
@app.template_filter('card_image')
def card_image_filter(card):
    return f"/static/cards/{card}.png"

if __name__ == '__main__':
    app.run(debug=True)
