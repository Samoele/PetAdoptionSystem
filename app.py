from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import date

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('pet_adoption.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# Basic Function: Search and List (join query + species/status filtering)
@app.route('/api/pets', methods=['GET'])
def get_pets():
    species = request.args.get('species', '')
    status = request.args.get('status', '')
    conn = get_db_connection()
    query = '''
        SELECT p.*, s.Name as ShelterName
        FROM Pets p
        LEFT JOIN Shelters s ON p.ShelterID = s.ShelterID
        WHERE 1=1
    '''
    params = []
    if species:
        query += ' AND p.Species LIKE ?'
        params.append(f'%{species}%')
    if status:
        query += ' AND p.AdoptionStatus = ?'
        params.append(status)
    pets = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(row) for row in pets])

# Basic Function: Insert a new pet
@app.route('/api/pets', methods=['POST'])
def add_pet():
    data = request.json
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO Pets (Name, Species, Breed, Age, ShelterID, Description, AdoptionStatus)
            VALUES (?, ?, ?, ?, ?, ?, 'Available')
        ''', (data['name'], data['species'], data.get('breed', ''),
              data.get('age', 0), data.get('shelter_id'), data.get('description', '')))
        conn.commit()
        return jsonify({'message': 'Pet added successfully!'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

# Basic Function: Update pet status
@app.route('/api/pets/<int:pet_id>', methods=['PUT'])
def update_pet(pet_id):
    data = request.json
    conn = get_db_connection()
    try:
        conn.execute('UPDATE Pets SET AdoptionStatus = ? WHERE PetID = ?',
                     (data['status'], pet_id))
        conn.commit()
        return jsonify({'message': 'Pet status updated!'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

# Basic Function: Delete a pet
@app.route('/api/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM Pets WHERE PetID = ?', (pet_id,))
        conn.commit()
        return jsonify({'message': 'Pet deleted!'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

# Aggregate Query: pet counts and average age grouped by shelter
@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT s.Name as ShelterName,
               COUNT(p.PetID) as TotalPets,
               SUM(CASE WHEN p.AdoptionStatus = 'Available' THEN 1 ELSE 0 END) as Available,
               SUM(CASE WHEN p.AdoptionStatus = 'Adopted'   THEN 1 ELSE 0 END) as Adopted,
               ROUND(AVG(p.Age), 1) as AvgAge
        FROM Shelters s
        LEFT JOIN Pets p ON s.ShelterID = p.ShelterID
        GROUP BY s.ShelterID, s.Name
        ORDER BY TotalPets DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# Adoption application (fixed: correct table name, correct column, fixed lastrowid for existing adopters)
@app.route('/api/adopt', methods=['POST'])
def adopt_pet():
    data = request.json
    pet_id = data['pet_id']
    adopter_name = data['adopter_name']
    adopter_email = data['adopter_email']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT OR IGNORE INTO Adopters (Name, ContactEmail) VALUES (?, ?)',
                       (adopter_name, adopter_email))
        adopter = conn.execute('SELECT AdopterID FROM Adopters WHERE ContactEmail = ?',
                               (adopter_email,)).fetchone()
        adopter_id = adopter['AdopterID']
        cursor.execute('UPDATE Pets SET AdoptionStatus = "Pending" WHERE PetID = ?', (pet_id,))
        cursor.execute('''
            INSERT INTO AdoptionApplications (AdopterID, PetID, AppDate, AppStatus)
            VALUES (?, ?, ?, 'Pending')
        ''', (adopter_id, pet_id, date.today().isoformat()))
        conn.commit()
        return jsonify({'message': 'Adoption application submitted successfully!'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
