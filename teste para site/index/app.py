from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

palavras = ['python', 'programacao', 'jogo', 'desenvolvimento', 'computador']

def escolher_palavra():
    return random.choice(palavras)

def exibir_palavra(palavra, letras_certas):
    exibicao = ''
    for letra in palavra:
        if letra in letras_certas:
            exibicao += letra + ' '
        else:
            exibicao += '_ '
    return exibicao.strip()

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'palavra' not in session:
        session['palavra'] = escolher_palavra()
        session['letras_certas'] = []
        session['letras_erradas'] = []
        session['tentativas'] = 6

    if request.method == 'POST':
        letra = request.form['letra'].lower()
        if letra in session['palavra']:
            session['letras_certas'].append(letra)
        else:
            session['letras_erradas'].append(letra)
            session['tentativas'] -= 1
        if set(session['letras_certas']) == set(session['palavra']):
            return redirect(url_for('ganhou'))
        if session['tentativas'] <= 0:
            return redirect(url_for('perdeu'))

    return render_template('index.html', palavra=exibir_palavra(session['palavra'], session['letras_certas']),
                           letras_erradas=session['letras_erradas'], tentativas=session['tentativas'])

@app.route('/novo_jogo')
def novo_jogo():
    session['palavra'] = escolher_palavra()
    session['letras_certas'] = []
    session['letras_erradas'] = []
    session['tentativas'] = 6
    return redirect(url_for('home'))

@app.route('/ganhou')
def ganhou():
    return render_template('ganhou.html', palavra=session['palavra'])

@app.route('/perdeu')
def perdeu():
    return render_template('perdeu.html', palavra=session['palavra'])

if __name__ == '__main__':
    app.run(debug=True)
