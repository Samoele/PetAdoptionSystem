# AdoptTallahassee — Pet Adoption System

A full-stack web application built for the Database Systems (COP 4710) course at Florida State University. The system centralizes pet adoption data from local Tallahassee shelters, allowing users to browse available pets, submit adoption applications, and find their best match through a compatibility recommender.

**Stack:** Python · Flask · SQLite3 · HTML/CSS · JavaScript

---

## Database Schema

**File:** `pet_adoption.db`

| Table | Key Columns | Notes |
|---|---|---|
| `Shelters` | ShelterID, Name, Location, ContactEmail | Parent table |
| `Pets` | PetID, Name, Species, Breed, Age, AdoptionStatus, ShelterID | FK → Shelters; CHECK constraint on status |
| `Adopters` | AdopterID, Name, ContactEmail, PhoneNumber, Address | UNIQUE on ContactEmail |
| `AdoptionApplications` | AppID, AdopterID, PetID, AppDate, AppStatus | FK → Adopters and Pets |

Foreign keys are enforced via `PRAGMA foreign_keys = ON`. The `Pets` table uses `ON DELETE SET NULL` on ShelterID and a `CHECK` constraint limiting AdoptionStatus to `'Available'`, `'Pending'`, or `'Adopted'`.

---

## Features

### Basic Functions
- **Insert** — Add new pets via the Manager page; submit adoption applications from the main site
- **Search & List** — Filter pets by species; results display shelter name via a `LEFT JOIN`
- **Join Query** — Every pet listing joins `Pets` and `Shelters` to show the shelter name
- **Aggregate Query** — Shelter overview computes total pets per shelter using `COUNT` + `GROUP BY`
- **Update** — Change a pet's adoption status from the Manager page
- **Delete** — Remove a pet listing from the Manager page

### Advanced Function — Compatibility Recommender
Users fill out a short lifestyle form (species preference, age group, activity level, living situation, owner experience) and receive every available pet ranked by a **0–100 compatibility score**. The score is computed entirely in SQL using five weighted `CASE` expressions over a `Pets JOIN Shelters` query, sorted descending by score. Results are displayed as a ranked list with a visual score bar.

---

## How to Run

**Prerequisites:** Python 3, pip

```bash
# 1. Install dependencies
pip install flask

# 2. Initialize the database (first time only)
python database.py

# 3. Start the Flask development server
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

The Manager page is at `http://127.0.0.1:5000/manager`.

---

## Project Structure

```
PetAdoptionSystem/
├── app.py              # Flask routes and API endpoints
├── database.py         # Schema creation and DB initialization
├── test_db.py          # CLI tool for inserting and querying data
├── pet_adoption.db     # SQLite database file
├── templates/
│   ├── index.html      # Main public-facing page
│   └── manager.html    # Admin/manager page
└── static/
    └── css/
        └── style.css   # Application styles
```

---

## Contributions — Ammiel Bowen

- Implemented the compatibility recommender (`/api/recommend`) — weighted multi-criteria scoring query using SQL `CASE` expressions joined across `Pets` and `Shelters`, with a ranked results UI and score bar
- Added species search filtering — wired the search input to a `LIKE` query parameter in the backend
- Fixed the adoption endpoint: corrected table name (`Applications` → `AdoptionApplications`), fixed the `lastrowid` bug for returning adopters, and added required `AppDate`/`AppStatus` fields
- Added missing CSS for the adopt modal (`.v-modal`, `.modal-content`, `.input-group`, `.v-btn-outline`) so it renders and displays correctly

---
