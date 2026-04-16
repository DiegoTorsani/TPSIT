from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurazione Database
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'localita'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# 1. Home - Corrisponde a index.php (Form di ricerca)
@app.route('/')
def index():
    return render_template('index.html')

# 2. Risultati - Corrisponde a risultati.php
@app.route('/risultati', methods=['GET'])
def risultati():
    termine = request.args.get('termine', '')
    if not termine:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query di ricerca
    query = "SELECT * FROM comuni WHERE name LIKE %s ORDER BY name ASC"
    cursor.execute(query, (f"%{termine}%",))
    comuni = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('risultati.html', comuni=comuni, termine=termine)

# 3. Dettaglio - Corrisponde a dettaglio.php
@app.route('/dettaglio/<int:comune_id>')
def dettaglio(comune_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Query con JOIN per ottenere Provincia e Regione (come nel file 289.jpg)
    query = """
        SELECT c.*, p.name AS provincia, r.name AS regione 
        FROM comuni c
        JOIN province p ON c.codice_provincia_istat = p.codice_provincia_istat
        JOIN regioni r ON p.codice_regione_istat = r.codice_regione_istat
        WHERE c.ID = %s
    """
    cursor.execute(query, (comune_id,))
    comune = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not comune:
        return "Comune non trovato", 404
        
    return render_template('dettaglio.html', comune=comune)

if __name__ == '__main__':
    app.run(debug=True)