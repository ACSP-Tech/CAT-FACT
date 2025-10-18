Cat Fact API
A production-ready FastAPI microservice that integrates user authentication with dynamic cat facts from an external API.
🚀 Live Demo
API Endpoint: https://acsp-cat-fact.pxxl.click/me
API Documentation: https://acsp-cat-fact.pxxl.click/docs
📋 Features

✅ RESTful API with FastAPI
✅ Async PostgreSQL database operations
✅ JWT-based authentication
✅ External API integration (Cat Facts API)
✅ Email validation with SendGrid
✅ Comprehensive error handling
✅ Request/response logging middleware
✅ Database migrations with Alembic
✅ Auto-generated API documentation

🛠️ Tech Stack

Framework: FastAPI
Database: PostgreSQL
ORM: SQLAlchemy (async)
Database Driver: asyncpg
Authentication: JWT (PyJWT)
Email Service: SendGrid
Migrations: Alembic
Validation: Pydantic
Deployment: Pxxl Cloud

📦 Prerequisites

Python 3.10 or higher
PostgreSQL 12 or higher
SendGrid API key (for email functionality)
Git

🔧 Installation & Setup
1. Clone the Repository
bashgit clone https://github.com/ACSP-Tech/CAT-FACT.git
cd CAT-FACT
2. Create Virtual Environment
bash# Create virtual environment
python -m venv Librarybox

# Activate virtual environment
# On Windows:
Librarybox\scripts\activate

# On macOS/Linux:
source venv/bin/activate
3. Install Dependencies
bashpip install --upgrade pip
pip install -r requirements.txt
4. Environment Variables
Create a .env file in the root directory:
bash# Database Configuration
DATABASE_URL=add yours 

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
bashpython -c "import secrets; print(secrets.token_urlsafe(64))"
5. Database Setup
bash# Create database
createdb catfact_db

# Run migrations
alembic upgrade head

# Create superadmin user (optional - run Python shell)
python
>>> from app.database_setup import get_session
>>> from app.model.cat_fact_db import Users
>>> # Create your superadmin user here
6. Run the Application
bash# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
The API will be available at: https://acsp-cat-fact.pxxl.click/
API documentation: https://acsp-cat-fact.pxxl.click/redoc
📝 API Endpoints
Main Endpoint
GET /api/me
Returns authenticated user information with a random cat fact.
Response:
json{
  "status": "success",
  "user": {
    "email": "user@example.com",
    "name": "John Doe",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-18T12:34:56.789Z",
  "fact": "Cats sleep 70% of their lives."
}
Other Endpoints

GET / - Root endpoint
GET /health - Health check
POST /api/users/register - User registration
GET /docs - Interactive API documentation (Swagger UI)
GET /redoc - Alternative API documentation

📚 Dependencies
Core dependencies (see requirements.txt for full list):
txtfastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy[asyncio]==2.0.23
asyncpg==0.29.0
alembic==1.13.1
pydantic[email]==2.5.0
PyJWT==2.8.0
python-decouple==3.8
sendgrid==6.11.0
requests==2.31.0
Install all dependencies:
bashpip install -r requirements.txt
🗂️ Project Structure
CAT-FACT/
├── alembic/                 # Database migrations
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application entry point
│   ├── database_setup.py   # Database configuration
│   ├── logging_config.py   # Logging setup
│   ├── sec.py              # Security configurations
│   ├── crud/               # Database operations
│   │   └── cat_fact.py
│   ├── middleware/         # Custom middleware
│   │   └── logging.py
│   ├── model/              # Database models
│   │   └── cat_fact_db.py
│   ├── routers/            # API routes
│   │   ├── cat_fact.py
│   │   └── add_user.py
│   └── schema/             # Pydantic models
│       └── cat_fact.py
├── .env                    # Environment variables (create this)
├── .gitignore
├── alembic.ini            # Alembic configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
🧪 Testing
Test the API endpoints:
bash# Health check - head request
curl https://acsp-cat-fact.pxxl.click/

# Main endpoint 
curl https://acsp-cat-fact.pxxl.click/me
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
VariableDescriptionRequiredDefaultDATABASE_URLPostgreSQL connection stringYes-SECRET_KEYJWT secret keyYes-ALGORITHMJWT algorithmNoHS256ACCESS_TOKEN_EXPIRE_MINUTESToken expiration timeNo30SENDGRID_API_KEYSendGrid API keyYes-CLOUD_ENVCloud environment flagNoFalseLOG_LEVELLogging levelNoINFO
🐛 Troubleshooting
Database Connection Error
bash# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Verify DATABASE_URL format
postgresql+asyncpg://username:password@host:port/database
Import Errors
bash# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
Port Already in Use
bash# Change port in uvicorn command
uvicorn app.main:app --port 8001
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


⭐ If you found this project helpful, please give it a star on GitHub!