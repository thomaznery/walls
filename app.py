from estrategias.RSIDolar import RSIDolar
from market.MarketData import MarketData
from flask import Flask, render_template
from flask import request

app = Flask(__name__)
md = MarketData()



@app.route("/", methods=['GET'])
def main():
    try:
        eRsi = RSIDolar()

        indice = str(md.ultimo_negocio("winq21")['preco'])
        dolar = str(md.ultimo_negocio('wdou21')['preco'])
    except Exception as e:
        print(e)
    return render_template('main.html', indice=indice, dolar=dolar, model=eRsi.__dict__)


def do_login():
    return render_template('login.html')


def show_login_form():
    return render_template('login_html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_login()
    else:
        return show_login_form()
