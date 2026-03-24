import string
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do Banco de Dados SQLite (será criado um arquivo 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

def gerar_codigo():
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(5))    


@app.route('/', methods=['GET', 'POST'])
def index():
    url_encurtada = None
    
    if request.method == 'POST':
        url_recebida = request.form['url_longa']
        
        codigo = gerar_codigo()
        
        novo_link = Link(original_url=url_recebida, short_code=codigo)
        db.session.add(novo_link)
        db.session.commit()
        
        url_encurtada = request.host_url + codigo
        
    return render_template('index.html', url_result=url_encurtada)

@app.route('/<codigo>')
def redirecionar(codigo):
    link_obj = Link.query.filter_by(short_code=codigo).first_or_404()
    return redirect(link_obj.original_url)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)