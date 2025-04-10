from flask import Flask, render_template, request, redirect, url_for, session
import random
from Blackjack.blackjack import deal_card, calculate_score, compare

app = Flask(__name__)
app.secret_key = 'hemlig_nyckel'  # Important for using sessions

@app.route('/', methods=['GET', 'POST'])
def index():
    # Start a new game if session does not have the player's hand
    if 'player_hand' not in session:
        session['player_hand'] = [deal_card(), deal_card()]
        session['computer_hand'] = [deal_card(), deal_card()]

    # Check if player chooses to hit or stand
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'hit':
            # Add a new card to player's hand
            session['player_hand'].append(deal_card())
        elif action == 'stand':
            # When stand is pressed, redirect to result page
            return redirect(url_for('result'))

    # Calculate score after each action
    player_score = calculate_score(session['player_hand'])

    return render_template('start.html', player_hand=session['player_hand'], player_score=player_score)

@app.route('/result')
def result():
    # Retrieve the player's and computer's hands
    player_hand = session['player_hand']
    computer_hand = session['computer_hand']

    player_score = calculate_score(player_hand)
    computer_score = calculate_score(computer_hand)

    # Computer draws cards until it reaches 17 or higher
    while computer_score < 17:
        computer_hand.append(deal_card())
        computer_score = calculate_score(computer_hand)

    result_message = compare(player_score, computer_score)  # Determine result of the game

    # Return the result page with all the details
    return render_template('result.html', result=result_message, 
                           player_hand=player_hand, player_score=player_score, 
                           computer_hand=computer_hand, computer_score=computer_score)

if __name__ == '__main__':
    app.run(debug=True)
