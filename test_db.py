import sqlite3

def get_connection():
    conn = sqlite3.connect('pet_adoption.db')
    conn.execute("PRAGMA foreign_keys = ON;") #Enables foreign key constraints for the connection, ensuring that any operations involving foreign keys will be properly enforced")
    return conn

def cli_menu():
    while True:
        print("Welcome to the Pet Adoption CLI!")
        print("Please select an option:")
        print("1. Add a Shelter")
        print("2. Add a Pet (Basic Function: Insert)")
        print("3. View All Pets with Shelter Info (Basic Function: Join)")
        print("4. Exit")
        
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Shelter Name: ")
            loc = input("Location: ")
            email = input("Contact Email: ")
            conn = get_connection()
            conn.execute("INSERT INTO Shelters (Name, Location, ContactEmail) VALUES (?, ?, ?)", (name, loc, email))
            conn.commit()
            print("Shelter added!")
            conn.close()

        elif choice == '2':
            # Note: You must have a ShelterID to add a pet because of the Foreign Key [cite: 11]
            name = input("Pet Name: ")
            species = input("Species: ")
            breed = input("Breed: ")
            age = input("Age: ")
            shelter_id = input("Shelter ID: ")
            
            try:
                conn = get_connection()
                conn.execute('''INSERT INTO Pets (Name, Species, Breed, Age, AdoptionStatus, ShelterID) 
                               VALUES (?, ?, ?, ?, 'Available', ?)''', 
                            (name, species, breed, age, shelter_id))
                conn.commit()
                print(f"Successfully inserted {name} into the database.")
            except sqlite3.IntegrityError:
                print("Error: That Shelter ID does not exist. Foreign Key constraint failed.") 
            finally:
                conn.close()

        elif choice == '3':
            print("\n--- Current Pets and their Shelters ---")
            conn = get_connection()
            # This implements the Join query required for your demo
            query = '''
                SELECT Pets.Name, Pets.Species, Shelters.Name 
                FROM Pets 
                JOIN Shelters ON Pets.ShelterID = Shelters.ShelterID
            '''
            results = conn.execute(query).fetchall()
            for row in results:
                print(f"Pet: {row[0]} | Species: {row[1]} | Shelter: {row[2]}")
            conn.close()

        elif choice == '4':
            break

if __name__ == "__main__":
    cli_menu()
