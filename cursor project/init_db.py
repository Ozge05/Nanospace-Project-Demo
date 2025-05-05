import psycopg2
from psycopg2 import Error
import os

def create_database():
    connection = None
    try:
        # PostgreSQL'e bağlan
        connection = psycopg2.connect(
            user="postgres",
            password="123456Aa",
            host="localhost",
            port="5432",
            database="postgres"  # Varsayılan veritabanı
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Veritabanını oluştur
        cursor.execute("DROP DATABASE IF EXISTS nanospace_db")
        cursor.execute("""
            CREATE DATABASE nanospace_db
            WITH 
            ENCODING = 'UTF8'
            TEMPLATE = template0;
        """)
        
        print("Veritabanı oluşturuldu!")
        
    except Error as e:
        print(f"Veritabanı oluşturma hatası: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def init_tables():
    connection = None
    try:
        # Yeni veritabanına bağlan
        connection = psycopg2.connect(
            user="postgres",
            password="123456Aa",
            host="localhost",
            port="5432",
            database="nanospace_db"  # Yeni oluşturulan veritabanı
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Tabloları oluştur
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS molecules (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            formula VARCHAR(100) NOT NULL,
            average_mass DECIMAL(10,3),
            monoisotopic_mass DECIMAL(10,3),
            chemspider_id VARCHAR(50),
            cas_number VARCHAR(50)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS synonyms (
            id SERIAL PRIMARY KEY,
            molecule_id INTEGER REFERENCES molecules(id),
            synonym VARCHAR(255) NOT NULL,
            language VARCHAR(50)
        )
        """)
        
        # Örnek veriyi ekle
        cursor.execute("""
        INSERT INTO molecules (name, formula, average_mass, monoisotopic_mass, chemspider_id, cas_number)
        VALUES (
            'Buckminsterfullerene',
            'C60',
            720.660,
            720.000,
            '110185',
            '99685-96-8'
        )
        """)
        
        cursor.execute("""
        INSERT INTO synonyms (molecule_id, synonym, language)
        VALUES 
            (1, '(5,6)Fullerene-C60-Ih', 'IUPAC'),
            (1, 'Buckminsterfullerene', 'English'),
            (1, 'C60 fullerene', 'English'),
            (1, 'Fullerene C60', 'English'),
            (1, 'Buckyball', 'English'),
            (1, 'バックミンスターフラーレン', 'Japanese'),
            (1, '富勒烯', 'Chinese'),
            (1, '버크민스터풀러렌', 'Korean')
        """)
        
        print("Tablolar ve örnek veriler oluşturuldu!")
        
    except Error as e:
        print(f"Tablo oluşturma hatası: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database()
    init_tables() 