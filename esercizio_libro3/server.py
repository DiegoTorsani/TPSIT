from flask import Flask, request, Response

app = Flask(__name__, static_folder='.', static_url_path='')

# Database temporaneo per la simulazione
prodotti = {
    'A123': {'prezzo': '250.00', 'marca': 'Asus', 'modello': 'Monitor 24"'},
    'B456': {'prezzo': '1200.00', 'marca': 'Lenovo', 'modello': 'ThinkPad'},
    'X789': {'prezzo': '85.50', 'marca': 'Logitech', 'modello': 'MX Master 3'}
}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/prodotto', methods=['GET'])
def get_prodotto():
    codice = request.args.get('codice', '').upper()
    
    # Prepara la risposta asincrona in formato HTML
    if codice in prodotti:
        p = prodotti[codice]
        html_data = f"""
        <ul>
            <li><strong>Prezzo:</strong> {p['prezzo']}</li>
            <li><strong>Marca:</strong> {p['marca']}</li>
            <li><strong>Modello:</strong> {p['modello']}</li>
        </ul>
        """
        return Response(html_data, mimetype='text/html')
    else:
        # Se non trovato, restituisce un errore 404
        return Response("Prodotto non trovato nel database.", status=404)

if __name__ == '__main__':
    app.run(debug=True, port=5000)