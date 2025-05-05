from flask import Flask, render_template, request, jsonify
from db_config import get_db_connection
from psycopg2 import Error
import sys
import locale
import traceback

# Karakter kodlaması ayarları
locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    connection = None
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Veritabanı bağlantısı kurulamadı'}), 500
            
        cursor = connection.cursor()
        
        # Molekül ve eş anlamlılarını ara
        cursor.execute("""
            SELECT m.*, s.synonym, s.language
            FROM molecules m
            LEFT JOIN synonyms s ON m.id = s.molecule_id
            WHERE m.name ILIKE %s 
            OR m.formula ILIKE %s 
            OR s.synonym ILIKE %s
        """, (f'%{query}%', f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        
        # Sonuçları düzenle
        molecules = {}
        for result in results:
            mol_id = result[0]
            if mol_id not in molecules:
                molecules[mol_id] = {
                    'id': result[0],
                    'name': result[1],
                    'formula': result[2],
                    'average_mass': result[3],
                    'monoisotopic_mass': result[4],
                    'chemspider_id': result[5],
                    'cas_number': result[6],
                    'synonyms': []
                }
            if result[7]:  # synonym varsa
                molecules[mol_id]['synonyms'].append({
                    'name': result[7],
                    'language': result[8]
                })
        
        return render_template('search.html', molecules=list(molecules.values()))
        
    except Error as e:
        print(f"Veritabanı hatası: {e}")
        print(f"Hata detayı: {traceback.format_exc()}")
        return jsonify({
            'error': 'Veritabanı hatası',
            'details': str(e)
        }), 500
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
        print(f"Hata detayı: {traceback.format_exc()}")
        return jsonify({
            'error': 'Beklenmeyen hata',
            'details': str(e)
        }), 500
    finally:
        if connection:
            connection.close()

@app.route('/molecule_detail')
def molecule_detail():
    return render_template('molecule_detail.html')

if __name__ == '__main__':
    app.run(debug=True) 