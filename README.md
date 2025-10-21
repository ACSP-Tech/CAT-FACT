String Analyzer + CAT FACT 
A production-ready FastAPI microservice that integrates user authentication with dynamic cat facts from an external API, plus a comprehensive string analysis tool with natural language query support.

🚀 Live Demo
API Endpoint: https://acsp-cat-fact.pxxl.click/me
API Documentation: https://acsp-cat-fact.pxxl.click/docs
ReDoc: https://acsp-cat-fact.pxxl.click/redoc
📋 Features
Core Features
✅ RESTful API with FastAPI
✅ Async PostgreSQL database operations
✅ JWT-based authentication
✅ External API integration (Cat Facts API)
✅ Email validation with SendGrid
✅ Comprehensive error handling
✅ Request/response logging middleware
✅ Database migrations with Alembic
✅ Auto-generated API documentation

String Analyzer Features
✅ String analysis with automatic property computation
✅ Natural language query filtering
✅ Advanced filtering by multiple criteria
✅ Palindrome detection
✅ Character frequency analysis
✅ SHA-256 hash generation
✅ Paginated results

🛠️ Tech Stack
Framework: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy (async) + SQLModel
Database Driver: asyncpg
Authentication: JWT (PyJWT)
Email Service: SendGrid
Migrations: Alembic
Validation: Pydantic
Pagination: fastapi-pagination
Deployment: Pxxl Cloud
📦 Prerequisites
Python 3.10 or higher
PostgreSQL 12 or higher
SendGrid API key (for email functionality)
Git
🔧 Installation & Setup
1. Clone the Repository
bash
git clone https://github.com/ACSP-Tech/CAT-FACT.git
cd CAT-FACT
2. Create Virtual Environment
bash
# Create virtual environment
python -m venv Librarybox

# Activate virtual environment
# On Windows:
Librarybox\Scripts\activate

# On macOS/Linux:
source Librarybox/bin/activate
3. Install Dependencies
bash
pip install --upgrade pip
pip install -r requirements.txt
4. Environment Variables
Create a .env file in the root directory:

bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/catfact_db

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Service
SENDGRID_API_KEY=your-sendgrid-api-key

# Logging
CLOUD_ENV=False
LOG_LEVEL=INFO
To generate a secure SECRET_KEY:

bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
5. Database Setup
bash
# Create database
createdb catfact_db

# Run migrations
alembic upgrade head
6. Run the Application
bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
The API will be available at:

Base URL: http://localhost:8000
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
📝 API Endpoints
Authentication & User Endpoints
Main Endpoint
GET /api/me
Returns authenticated user information with a random cat fact.

Response:

json
{
  "status": "success",
  "user": {
    "email": "user@example.com",
    "name": "John Doe",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-21T12:34:56.789Z",
  "fact": "Cats sleep 70% of their lives."
}
Other User Endpoints
GET / - Root endpoint
GET /health - Health check
POST /api/users/register - User registration
String Analysis Endpoints
Create String Analysis
POST /strings

Creates and analyzes a new string with automatic property computation.

Request Body:

json
{
  "value": "hello world"
}
Response (201 Created):

json
{
  "id": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
  "value": "hello world",
  "properties": {
    "length": 11,
    "is_palindrome": false,
    "unique_characters": 8,
    "word_count": 2,
    "sha256_hash": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
    "character_frequency_map": {
      "h": 1,
      "e": 1,
      "l": 3,
      "o": 2,
      " ": 1,
      "w": 1,
      "r": 1,
      "d": 1
    }
  },
  "created_at": "2025-10-21T12:34:56.789Z"
}
Validations:

Value cannot be empty
Leading/trailing spaces are trimmed
No consecutive spaces allowed
Converted to lowercase for case-insensitive matching
Get Single String
GET /strings/{string_value}

Retrieves a specific string analysis by its value.

Example:

bash
GET /strings/hello
Get All Strings (Paginated)
GET /strings/search/all

Returns all analyzed strings with pagination support.

Query Parameters:

page (optional, default: 1) - Page number
size (optional, default: 50) - Items per page
Response:

json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 50,
  "pages": 2
}
Filter Strings
GET /strings

Advanced filtering with multiple criteria.

Query Parameters:

is_palindrome (boolean, optional) - Filter by palindrome status
min_length (integer, optional) - Minimum string length
max_length (integer, optional) - Maximum string length
word_count (integer, optional) - Exact word count
contains_character (string, optional) - Character or substring to search for
Example:

bash
GET /strings?is_palindrome=true&min_length=3&max_length=10
Response:

json
{
  "data": [
    {
      "id": "...",
      "value": "racecar",
      "properties": {...},
      "created_at": "2025-10-21T12:34:56.789Z"
    }
  ],
  "count": 5,
  "filters_applied": {
    "is_palindrome": true,
    "min_length": 3,
    "max_length": 10
  }
}
Natural Language Query
GET /strings/filter-by-natural-language

Filter strings using natural language queries powered by AI interpretation.

Query Parameters:

query (string, required) - Natural language query
Examples:

bash
# Find palindromes
GET /strings/filter-by-natural-language?query=all palindromic strings

# Find single word palindromes
GET /strings/filter-by-natural-language?query=all single word palindromic strings

# Find strings with length constraints
GET /strings/filter-by-natural-language?query=strings longer than 5 characters

# Find strings containing specific characters
GET /strings/filter-by-natural-language?query=strings containing the letter a
Response:

json
{
  "data": [...],
  "count": 10,
  "interpreted_query": {
    "original": "all single word palindromic strings",
    "parsed_filters": {
      "is_palindrome": true,
      "word_count": 1
    }
  }
}
Delete String
DELETE /strings/{string_value}

Deletes a specific string from the system.

Response: 204 No Content

📚 Dependencies
Core dependencies (see requirements.txt for full list):

txt
fastapi==0.119.0
uvicorn==0.37.0
sqlalchemy==2.0.44
sqlmodel==0.0.27
asyncpg==0.30.0
alembic==1.17.0
pydantic==2.12.3
email-validator==2.3.0
PyJWT==2.10.1
python-decouple==3.8
sendgrid==6.12.5
requests==2.32.5
fastapi-pagination==0.14.3
psycopg2==2.9.11
cryptography==46.0.3
Install all dependencies:

bash
pip install -r requirements.txt
🗂️ Project Structure
CAT-FACT/
├── alembic/                    # Database migrations
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   ├── database_setup.py      # Database configuration
│   ├── logging_config.py      # Logging setup
│   ├── sec.py                 # Security configurations
│   ├── crud/                  # Database operations
│   │   ├── cat_fact.py
│   │   └── string_analysis.py # String analyzer CRUD
│   ├── middleware/            # Custom middleware
│   │   └── logging.py
│   ├── model/                 # Database models
│   │   └── cat_fact_db.py    # User & StringAnalysis models
│   ├── routers/               # API routes
│   │   ├── cat_fact.py
│   │   ├── add_user.py
│   │   └── string_analysis.py # String analyzer routes
│   ├── schema/                # Pydantic models
│   │   ├── cat_fact.py
│   │   └── string_analysis.py # String analyzer schemas
│   └── utils/                 # Utility functions
│       └── string_analysis.py # NL query parser
├── .env                       # Environment variables
├── .gitignore
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
🧪 Testing
Test the API endpoints:

bash
# Health check
curl https://acsp-cat-fact.pxxl.click/

# Main endpoint
curl https://acsp-cat-fact.pxxl.click/me

# Create string analysis
curl -X POST https://acsp-cat-fact.pxxl.click/strings \
  -H "Content-Type: application/json" \
  -d '{"value": "racecar"}'

# Get string analysis
curl https://acsp-cat-fact.pxxl.click/strings/racecar

# Filter palindromes
curl "https://acsp-cat-fact.pxxl.click/strings?is_palindrome=true"

# Natural language query
curl "https://acsp-cat-fact.pxxl.click/strings/filter-by-natural-language?query=all%20palindromic%20strings"
🚢 Deployment
The application is deployed on Pxxl Cloud. To deploy your own instance:

Create account on Pxxl.app
Connect your GitHub repository
Configure environment variables in Pxxl dashboard
Set build commands:
Install: python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt
Build: Leave empty
Start: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
🔒 Environment Variables Reference
Variable	Description	Required	Default
DATABASE_URL	PostgreSQL connection string	Yes	-
SECRET_KEY	JWT secret key	Yes	-
ALGORITHM	JWT algorithm	No	HS256
ACCESS_TOKEN_EXPIRE_MINUTES	Token expiration time	No	30
SENDGRID_API_KEY	SendGrid API key	Yes	-
CLOUD_ENV	Cloud environment flag	No	False
LOG_LEVEL	Logging level	No	INFO
🐛 Troubleshooting
Database Connection Error
bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Verify DATABASE_URL format
postgresql+asyncpg://username:password@host:port/database
Import Errors
bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
Port Already in Use
bash
# Change port in uvicorn command
uvicorn app.main:app --port 8001
Route Conflicts
The string analysis routes are ordered specifically to avoid path conflicts:

/strings/filter-by-natural-language (most specific)
/strings/search/all (specific path)
/strings/{string_value} (dynamic parameter - must be last)
📄 License
This project is open source and available under the MIT License.

👤 Author
Precious Chioma Aguluka

GitHub: @ACSP-Tech
Email: acspworld@gmail.com
🙏 Acknowledgments
FastAPI for the amazing framework
Cat Facts API for the cat facts
ACSP Tech community for support
⭐ Star This Project
If you found this project helpful, please give it a star on GitHub!

Built with love using FastAPI