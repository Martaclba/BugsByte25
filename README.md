# 🐞 BugsByte25

BugsByte25 is a full-stack **recipe recommendation system** developed during the _BugsByte Hackathon_ (March 2025, Fórum Braga). It uses a hybrid machine learning model (collaborative + content-based filtering) to suggest recipes based on users’ purchase history and ingredient preferences. The platform also provides price-aware product suggestions, helping users discover new meals, shop smarter, and reduce food waste.

The system is built with a **Python/Flask backend**, a **Next.js/React frontend**, and **SingleStoreDB**, which is used both as a vector database for the recommendation models and as a relational database for storing user data, recipes, and transactions. The backend exposes RESTful APIs for retrieving users, bundles of recipes, and individual recipe details.


# Project Structure

```
BugsByte25/
├── backend/ 
│ ├── src/
│ │ ├── main.py
│ │ ├── model.py → Recommendation models
│ │ ├── retrieval.py → Data retrieval logic
│ │ ├── setup_db.py → Database setup
│ │ └── populate_db.py → Initial database population
│ ├── requirements.txt
│ ├── Dockerfile
│ ├── compose.yml
│ └── start.sh / setup.sh
│
├── frontend/ (Next.js + TypeScript)
│ ├── src/app/
│ ├── src/components/
│ ├── src/lib/
│ ├── public/
│ └── package.json
│
└── README.md
```


# Technologies Used

## Backend

- Python 3 with Flask and Flask-RESTful
- SingleStoreDB for vector storage (recommendation models) and relational data (users, recipes, transactions)
- Docker & Docker Compose for deployment
- RESTful API exposing endpoints for users, recipe bundles, and individual recipes
 
## Frontend

- Next.js 13 (App Router)
- React + TypeScript
- TailwindCSS / PostCSS
- pnpm or npm for package management


# How to Run

### Clone the repository:

```
git clone https://github.com/your-username/BugsByte25.git
cd BugsByte25
```

## Backend

```
cd backend
./setup.sh
./start.sh
```

API available at: http://localhost:8000


## Frontend

```
cd frontend
npm install
npm run dev
```
Frontend available at: http://localhost:3000

# Features

- Hybrid recommendation system (content-based + collaborative filtering).
- Intuitive web interface built with Next.js.
- Integration with a vector database for efficient storage and retrieval.
- Fast and scalable APIs with Docker support.

# Contributing

- Fork the repository.
- Create a branch: git checkout -b feature/feature-name
- Commit your changes: git commit -m "feat: description of feature"
- Push to the branch: git push origin feature/feature-name
- Open a Pull Request.

# License
This project is licensed under the GNU General Public License v3.0 (see backend/LICENSE).x