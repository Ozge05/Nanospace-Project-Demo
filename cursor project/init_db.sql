-- Veritabanını oluştur (eğer yoksa)
CREATE DATABASE nanospace_db
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'tr_TR.UTF-8'
    LC_CTYPE = 'tr_TR.UTF-8'
    TEMPLATE = template0;

-- Molekül tablosu
CREATE TABLE IF NOT EXISTS molecules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    formula VARCHAR(100) NOT NULL,
    average_mass DECIMAL(10,3),
    monoisotopic_mass DECIMAL(10,3),
    chemspider_id VARCHAR(50),
    cas_number VARCHAR(50)
);

-- Molekül eş anlamlıları tablosu
CREATE TABLE IF NOT EXISTS synonyms (
    id SERIAL PRIMARY KEY,
    molecule_id INTEGER REFERENCES molecules(id),
    synonym VARCHAR(255) NOT NULL,
    language VARCHAR(50)
);

-- Örnek veri ekleme
INSERT INTO molecules (name, formula, average_mass, monoisotopic_mass, chemspider_id, cas_number)
VALUES (
    'Buckminsterfullerene',
    'C60',
    720.660,
    720.000,
    '110185',
    '99685-96-8'
);

-- Eş anlamlıları ekleme
INSERT INTO synonyms (molecule_id, synonym, language)
VALUES 
    (1, '(5,6)Fullerene-C60-Ih', 'IUPAC'),
    (1, 'Buckminsterfullerene', 'English'),
    (1, 'C60 fullerene', 'English'),
    (1, 'Fullerene C60', 'English'),
    (1, 'Buckyball', 'English'),
    (1, 'バックミンスターフラーレン', 'Japanese'),
    (1, '富勒烯', 'Chinese'),
    (1, '버크민스터풀러렌', 'Korean'); 