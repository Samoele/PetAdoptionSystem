from flask import Flask, render_template, request, jsonify
import sqlite3


#basic code implemented using gemini ai foor database connection and flask app setup. The rest of the code is written by me, but I used gemini to help me with the basic structure and some of the queries. 
app = Flask(__name__)

# Helper to connect to the database you just tested
def get_db_connection():
    conn = sqlite3.connect('pet_adoption.db')
    conn.row_factory = sqlite3.Row # This allows us to use column names in our code
    return conn

@app.route('/')
def index():
    # This serves the main HTML page to the user
    return render_template('index.html')

# Basic Function: Search and List
@app.route('/api/pets', methods=['GET'])
def get_pets():
    conn = get_db_connection()
    # Joining Pets and Shelters for the demo requirement [cite: 44]
    query = '''
        SELECT p.*, s.Name as ShelterName 
        FROM Pets p 
        LEFT JOIN Shelters s ON p.ShelterID = s.ShelterID
    '''
    pets = conn.execute(query).fetchall()
    conn.close()
    
    # Convert database rows to a list of dictionaries for the frontend
    return jsonify([dict(ix) for ix in pets])

@app.route('/api/adopt', methods=['POST'])
def adopt_pet():
    data = request.json
    pet_id = data['pet_id']
    adopter_name = data['adopter_name']
    adopter_email = data['adopter_email']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        #insert adopter info into Adopters table, using INSERT OR IGNORE to avoid duplicates based on unique email constraint [cite: 5]
        cursor.execute ('INSERT OR IGNORE INTO Adopters (Name, Email) VALUES (?, ?)', (adopter_name, adopter_email))
        adopter_id = cursor.lastrowid # Get the AdopterID of the newly inserted adopter or existing one

        #Update pets status
        cursor.execute('UPDATE Pets SET AdoptionStatus = "Pending" WHERE PetID = ?', (pet_id))
        
        #Create application
        cursor.execute('INSERT INTO Applications (PetID, AdopterID) VALUES (?, ?)', (pet_id, adopter_id))
        conn.commit()

        return jsonify({'message': 'Adoption application submitted successfully!'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400  
        
if __name__ == '__main__':
    app.run(debug=True)