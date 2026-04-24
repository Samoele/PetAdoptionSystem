from flask import Flask, render_template, request, jsonify
from datetime import datetime
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

@app.route('/manager') #Manager page
def manage_page():
    return render_template('manager.html')

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


# Basic Function: Aggregate Query and Shelter fetch 
@app.route('/api/shelter-stats', methods=['GET'])
def get_shelter_stats():
    conn = get_db_connection()
    # AGGREGATE QUERY: Counts pets per shelter while joining shelter info 
    query = '''
        SELECT s.ShelterID, s.Name, s.Location, s.ContactEmail, 
               COUNT(p.PetID) as TotalPets
        FROM Shelters s
        LEFT JOIN Pets p ON s.ShelterID = p.ShelterID
        GROUP BY s.ShelterID
    '''
    stats = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in stats])

#Function for deleting pets
@app.route('/api/pets/<int:pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM Pets WHERE PetID = ?', (pet_id,))
        conn.commit()
        return jsonify({"message": "Deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


#Function for adding pets from manager page
@app.route('/api/pets', methods=['POST'])
def add_pet():
    data = request.json
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO Pets (Name, Species, Breed, Age, AdoptionStatus, ShelterID)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['species'], data['breed'], data['age'], data['status'], data['shelter_id']))
        conn.commit()
        return jsonify({"message": "Pet added!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@app.route('/api/adopt', methods=['POST'])
def adopt_pet():
    data = request.json
    pet_id = data['pet_id']
    adopter_name = data['adopter_name']
    adopter_email = data['adopter_email']
    adopter_phone = data.get('adopter_phone')
    adopter_address = data.get('adopter_address')

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        #insert adopter info into Adopters table, using INSERT OR IGNORE to avoid duplicates based on unique email constraint [cite: 5]
        cursor.execute ('INSERT OR IGNORE INTO Adopters (Name, ContactEmail, Address, PhoneNumber) VALUES (?, ?, ?, ?)', (adopter_name, adopter_email, adopter_phone, adopter_address))
        adopter_id = cursor.lastrowid # Get the AdopterID of the newly inserted adopter or existing one

        #Update pets status
        cursor.execute('UPDATE Pets SET AdoptionStatus = "Pending" WHERE PetID = ?', (pet_id))
        
        #Create application
        cursor.execute('INSERT INTO AdoptionApplications (PetID, AdopterID, AppDate, AppStatus) VALUES (?, ?, ?, "Under Review")', (pet_id, adopter_id, current_date))
        
        #Deletion of pets
        
        
        
        
        conn.commit()

        return jsonify({'message': 'Adoption application submitted successfully!'})
    except Exception as e:
            conn.rollback()
            print(f"DATABASE ERROR: {e}") # This will print the exact reason in your terminal
            return jsonify({"error": str(e)}), 400
        
if __name__ == '__main__':
    app.run(debug=True)