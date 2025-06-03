from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Página inicial já carrega o index.html
@app.route("/")
def index():
    return render_template("index.html")

# Servir arquivos de imagem, som, etc.
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(debug=True)
