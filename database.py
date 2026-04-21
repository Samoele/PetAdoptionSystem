import sqlite3

def init_db(): #Connects to the SQLite database file named 'pet_adoption.db'. If the file does not exist, it will be created.
    conn = sqlite3.connect('pet_adoption.db') 
    cursor = conn.cursor()
    
    #Enables foreign key constraints usually disabled by default in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

#tables for database in orders of dependencies
    #Shelters table to store information about pet shelters, including shelter ID, name, location, and contact email.  
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Shelters (
            ShelterID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Location TEXT NOT NULL,
            ContactEmail TEXT);
    ''')

    #Pets table to store information about pets available for adoption, including pet ID, name, species, breed, age, shelter ID (foreign key), and adoption status.
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Pets (
        PetID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Species TEXT NOT NULL,
        Breed TEXT,
        Age INTEGER,
        ShelterID INTEGER,
        Description TEXT,
        AdoptionStatus TEXT NOT NULL CHECK(AdoptionStatus IN ('Available', 'Adopted', 'Pending')),
        FOREIGN KEY (ShelterID) REFERENCES Shelters(ShelterID) ON DELETE SET NULL);
    ''') 
    
    #Adopters table to store information about individuals who adopt pets, including adopter ID, name, contact email, and phone number.
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Adopters (
        AdopterID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        ContactEmail TEXT UNIQUE,
        PhoneNumber TEXT,
        Address TEXT)
    ''')

    #AdoptionApplications table to store information about adoption applications, including application ID, adopter ID (foreign key), pet ID (foreign key), application date, and application status.
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS AdoptionApplications (
        AppID INTEGER PRIMARY KEY AUTOINCREMENT,
        AdopterID INTEGER,
        PetID INTEGER,
        AppDate TEXT NOT NULL,
        AppStatus TEXT NOT NULL,
        FOREIGN KEY (AdopterID) REFERENCES Adopters(AdopterID), 
        FOREIGN KEY (PetID) REFERENCES Pets(PetID))
    ''')


    conn.commit() #Commits the changes to the database, ensuring that the tables are created and any modifications are saved.
    conn.close() #Closes the connection to the database
    print("Database initialized successfully.")

if __name__ == "__main__":    
    init_db() #Calls the init_db function to initialize the database when the script is run directly.

