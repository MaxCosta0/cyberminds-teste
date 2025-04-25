from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Pasta onde as imagens serão salvas
UPLOAD_FOLDER = os.path.join('static', 'imagens')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS imagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caminho TEXT,
            descricao TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Página principal: exibe todas as imagens
@app.route("/")
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT caminho, descricao, id FROM imagens")
    imagens = c.fetchall()
    conn.close()
    return render_template("index.html", imagens=imagens)

# Página de upload: formulário para adicionar novas imagens
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        descricao = request.form["descricao"]
        imagem = request.files["imagem"]

        if imagem:
            filename = secure_filename(imagem.filename)
            caminho = os.path.join(UPLOAD_FOLDER, filename)
            imagem.save(caminho)

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO imagens (caminho, descricao) VALUES (?, ?)",
                      (caminho, descricao))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))
    return render_template("upload.html")

@app.route("/delete/<int:imagem_id>", methods=["POST"])
def delete(imagem_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT caminho FROM imagens WHERE id = ?", (imagem_id,))
    imagem = c.fetchone()
    
    if imagem:
        caminho = imagem[0]
        if os.path.exists(caminho):
            os.remove(caminho)
        c.execute("DELETE FROM imagens WHERE id = ?", (imagem_id,))
        conn.commit()

    conn.close()
    return redirect(url_for('index'))


# Executa o app
if __name__ == "__main__":
    app.run(debug=True)
