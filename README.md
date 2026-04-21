# PetAdoptionSystem
Pet adoption website for Databases final project

# Pet Adoption System - Tallahassee

A sophisticated full-stack web application developed for the Database Systems course at Florida State University. This system centralizes pet data from local shelters in Tallahassee to streamline the adoption process through a high-end, editorial-style interface.

## 🗄️ Database Architecture
[cite_start]The project utilizes a relational database designed to maintain strict data integrity and enforce complex relationships between entities[cite: 5].

**Database File:** `pet_adoption.db` (SQLite3)

### [cite_start]Tables and Relational Schema[cite: 6, 12, 14]:
* **Shelters**: Contains core organizational data (ShelterID, Name, Location, ContactEmail)[cite: 6].
* **Pets**: Stores detailed animal profiles (PetID, Name, Species, Breed, Age, Description, AdoptionStatus, ShelterID)[cite: 10]. 
    * *Constraint*: Enforces `ON DELETE SET NULL` and `CHECK` constraints on status.
* **Adopters**: Manages user contact records (AdopterID, Name, Email, Phone, Address)[cite: 12].
* **Applications**: A junction table linking Adopters to Pets (AppID, AdopterID, PetID, AppDate, AppStatus).

## 🚀 How to Run the Flask Web Server
[cite_start]Running the Flask server is the "glue" that connects the SQLite3 database to the web interface[cite: 27, 28].

### 1. Environment Setup
Ensure Python 3 is installed. It is highly recommended to use a virtual environment (`venv`).
```bash
# Install Flask
pip install flask
