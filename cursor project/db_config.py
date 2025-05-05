import psycopg2
from psycopg2 import Error

def get_db_connection():
    try:
        # Bağlantı parametrelerini bir dictionary olarak tanımla
        conn_params = {
            'dbname': 'nanospace_db',
            'user': 'postgres',
            'password': '123456Aa',
            'host': 'localhost',
            'port': '5432',
            'client_encoding': 'UTF8'
        }
        
        # Bağlantıyı oluştur
        connection = psycopg2.connect(**conn_params)
        
        # Bağlantı ayarlarını yapılandır
        connection.set_client_encoding('UTF8')
        
        return connection
    except Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None 