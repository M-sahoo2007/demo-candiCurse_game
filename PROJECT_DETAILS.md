# CandyVerse - Complete Project Documentation

**Date**: May 17, 2026  
**Status**: Production Ready  
**Version**: 1.0.0

---

## 📖 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [Running the Project](#running-the-project)
7. [Database Schema](#database-schema)
8. [API Documentation](#api-documentation)
9. [File Descriptions](#file-descriptions)
10. [User Management](#user-management)
11. [Game Mechanics](#game-mechanics)
12. [Leaderboard System](#leaderboard-system)
13. [Development Workflow](#development-workflow)
14. [Troubleshooting](#troubleshooting)

---

## 🎮 Project Overview

### What is CandyVerse?

CandyVerse is a **web-based candy game platform** where users can:
- Play interactive candy-themed games
- Earn points and compete globally
- Track progress on a leaderboard
- Manage their user profiles
- View real-time rankings

It's built with **Django** (backend), **HTML/CSS/JavaScript** (frontend), and **SQLite/PostgreSQL** (database).

### Project Goals

✅ Provide engaging candy-themed gameplay  
✅ Real-time leaderboard tracking  
✅ User authentication & profiles  
✅ REST API for mobile/external apps  
✅ Responsive web interface  
✅ Easy deployment to cloud platforms  

### Target Audience

- Casual gamers aged 8+
- Competitive players seeking rankings
- Mobile users accessing web app
- API consumers building integrations

---

## 🌟 Features

### 1. **User Management**
- User registration with email validation
- Secure login/logout
- Password reset via email
- User profile with avatar
- Account settings management
- User statistics (games played, total points)

### 2. **Game System**
- Multiple candy-themed mini-games
- Point earning system
- Game progress tracking
- Daily challenges
- Achievement badges
- Game history

### 3. **Leaderboard**
- Global rankings by points
- Weekly/monthly leaderboards
- Regional rankings
- Personal statistics
- Friend comparisons
- Top 100 rankings

### 4. **Social Features**
- User profiles
- Friend system (if implemented)
- Achievement sharing
- Competition tracking

### 5. **Admin Panel**
- User management
- Game statistics
- Leaderboard moderation
- Site settings
- Report management

---

## 🛠 Technology Stack

### Backend
- **Django 3.2+**: Web framework
- **Django REST Framework**: API endpoints
- **PostgreSQL/SQLite**: Database
- **Gunicorn**: WSGI application server
- **Nginx**: Reverse proxy (production)

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling
- **JavaScript (Vanilla)**: Interactivity
- **Bootstrap 5**: Responsive design (optional)

### Deployment
- **Docker**: Containerization
- **Railway/Render**: Hosting
- **AWS S3**: Media storage (optional)
- **GitHub**: Version control
- **GitHub Actions**: CI/CD

### Development Tools
- **Python 3.9+**: Programming language
- **pip**: Package manager
- **Virtual Environment**: Dependency isolation
- **Postman**: API testing
- **SQLite Admin**: Database management

---

## 📁 Project Structure

```
CandyVerse/
│
├── candyverse/              # Django project configuration
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
├── api/                     # REST API app
│   ├── __init__.py
│   ├── apps.py
│   ├── serializers.py       # API serializers
│   ├── urls.py              # API routes
│   ├── views.py             # API views
│   └── migrations/
│
├── game/                    # Game logic app
│   ├── __init__.py
│   ├── admin.py             # Django admin config
│   ├── apps.py
│   ├── models.py            # Game models
│   ├── urls.py              # Game URLs
│   ├── views.py             # Game views
│   └── migrations/
│
├── leaderboard/             # Leaderboard app
│   ├── __init__.py
│   ├── admin.py             # Admin config
│   ├── apps.py
│   ├── models.py            # Leaderboard models
│   ├── urls.py              # Leaderboard URLs
│   ├── views.py             # Leaderboard views
│   └── migrations/
│
├── users/                   # User management app
│   ├── __init__.py
│   ├── admin.py             # Admin config
│   ├── apps.py
│   ├── forms.py             # Registration/login forms
│   ├── models.py            # User models
│   ├── serializers.py       # API serializers
│   ├── urls.py              # User URLs
│   ├── views.py             # User views
│   └── migrations/
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── home.html            # Home page
│   ├── game.html            # Game page
│   ├── leaderboard.html     # Leaderboard page
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── profile.html         # User profile
│   ├── 404.html             # Error page
│   └── 500.html             # Error page
│
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   └── js/
│       ├── game.js          # Game logic
│       └── scripts.js       # Helper functions
│
├── media/                   # User uploads (avatars, etc.)
│
├── docs/                    # Documentation
│   └── deployment.md        # Deployment guide
│
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose config
├── Procfile                 # Procfile for Heroku/Railway
├── README.md                # Quick start guide
└── .env.example             # Environment variables template
```

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment tool
- Git

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/candyverse.git
cd CandyVerse
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create `.env` file in project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
STATIC_URL=/static/
MEDIA_URL=/media/
```

### Step 5: Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Enter: username, email, password
```

### Step 6: Create Sample Data (Optional)

```bash
# Load fixtures if available
python manage.py loaddata initial_data
```

### Step 7: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 🚀 Running the Project

### Development Server

```bash
python manage.py runserver
# Access at http://localhost:8000
```

### Production Server (Gunicorn)

```bash
gunicorn candyverse.wsgi:application --bind 0.0.0.0:8000
```

### Docker

```bash
# Build image
docker build -t candyverse:1.0 .

# Run container
docker run -p 8000:8000 candyverse:1.0
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

---

## 📊 Database Schema

### Users App

#### User Model (extends Django User)
```python
class UserProfile:
    - user (OneToOne) → Django User
    - avatar (ImageField) → Profile picture
    - bio (TextField) → User biography
    - total_points (IntegerField) → Career total points
    - games_played (IntegerField) → Total games
    - created_at (DateTimeField) → Account creation
    - updated_at (DateTimeField) → Last update
```

### Game App

#### Game Model
```python
class Game:
    - title (CharField) → Game name
    - description (TextField) → Game description
    - instructions (TextField) → How to play
    - max_score (IntegerField) → Maximum possible score
    - created_at (DateTimeField)
    - is_active (BooleanField) → Published status
```

#### GameScore Model
```python
class GameScore:
    - user (ForeignKey) → User who played
    - game (ForeignKey) → Game played
    - score (IntegerField) → Points earned
    - played_at (DateTimeField) → When played
    - duration (IntegerField) → Game duration (seconds)
    - completed (BooleanField) → Game finished status
```

### Leaderboard App

#### LeaderboardEntry Model
```python
class LeaderboardEntry:
    - user (ForeignKey) → User
    - rank (IntegerField) → Current rank
    - total_points (IntegerField) → Points from all games
    - games_played (IntegerField) → Game count
    - last_played (DateTimeField) → Last game date
    - weekly_points (IntegerField) → This week's points
    - monthly_points (IntegerField) → This month's points
```

### Relationships
```
User (1) ──→ (Many) UserProfile
User (1) ──→ (Many) GameScore
User (1) ──→ (One) LeaderboardEntry
Game (1) ──→ (Many) GameScore
```

---

## 🔌 API Documentation

### Base URL
```
Development: http://localhost:8000/api/
Production: https://yourdomain.com/api/
```

### Authentication
- Session-based (cookies)
- Token-based (if implemented)

### Endpoints

#### User Endpoints
```
GET    /api/users/                   # List all users
POST   /api/users/                   # Create user
GET    /api/users/{id}/              # Get user details
PUT    /api/users/{id}/              # Update user
DELETE /api/users/{id}/              # Delete user
GET    /api/users/{id}/profile/      # Get user profile
POST   /api/users/register/          # Register new user
POST   /api/users/login/             # Login user
POST   /api/users/logout/            # Logout user
```

#### Game Endpoints
```
GET    /api/games/                   # List all games
GET    /api/games/{id}/              # Get game details
POST   /api/games/{id}/play/         # Start game
PUT    /api/games/{id}/score/        # Submit score
GET    /api/games/{id}/scores/       # Get game leaderboard
```

#### Leaderboard Endpoints
```
GET    /api/leaderboard/             # Get global leaderboard
GET    /api/leaderboard/weekly/      # Get weekly leaderboard
GET    /api/leaderboard/monthly/     # Get monthly leaderboard
GET    /api/leaderboard/user/{id}/   # Get user ranking
```

### Example API Response

```json
{
  "id": 1,
  "username": "candymaster",
  "email": "user@example.com",
  "total_points": 5420,
  "games_played": 24,
  "rank": 15,
  "profile": {
    "avatar": "/media/avatars/user1.jpg",
    "bio": "Candy game enthusiast!"
  },
  "created_at": "2026-01-15T10:30:00Z"
}
```

---

## 📄 File Descriptions

### Backend Files

#### `candyverse/settings.py`
- Django configuration
- Database settings
- Installed apps
- Middleware
- Static/media files
- Email settings
- Security settings

#### `candyverse/urls.py`
- Main URL routing
- Includes app URLs
- Admin interface
- Static file serving

#### `users/models.py`
- UserProfile model
- User-related fields
- Methods for user operations

#### `users/views.py`
- Registration view
- Login/logout views
- Profile management
- Password reset

#### `game/models.py`
- Game model definition
- GameScore model
- Achievement model (if included)

#### `game/views.py`
- Game listing
- Game play view
- Score submission
- Game statistics

#### `leaderboard/models.py`
- LeaderboardEntry model
- Ranking calculations
- Weekly/monthly rankings

#### `api/serializers.py`
- REST serializers for models
- Field validation
- Data transformation

#### `api/views.py`
- API viewsets
- REST endpoints
- Authentication handling

### Frontend Files

#### `templates/base.html`
- Base template with navbar
- CSS/JS imports
- Block definitions
- Footer

#### `templates/game.html`
- Game interface
- Game canvas/area
- Score display
- Game controls
- JavaScript integration

#### `templates/leaderboard.html`
- Leaderboard table
- Rankings display
- User statistics
- Filtering options

#### `templates/profile.html`
- User profile display
- Statistics summary
- Avatar
- Account settings link

#### `templates/login.html`
- Login form
- Email/password fields
- Remember me option
- Registration link

#### `templates/register.html`
- Registration form
- Field validation
- Agreement checkbox
- Login link

#### `static/css/style.css`
- Main stylesheet
- Responsive design
- Game styling
- Component styles

#### `static/js/game.js`
- Game logic
- Canvas drawing
- Event handling
- Score tracking
- Game state management

#### `static/js/scripts.js`
- Utility functions
- DOM manipulation
- API calls
- Form validation

### Configuration Files

#### `requirements.txt`
```
Django==3.2.0
djangorestframework==3.12.4
python-decouple==3.4
Pillow==8.2.0
psycopg2-binary==2.8.6
gunicorn==20.1.0
```

#### `Dockerfile`
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "candyverse.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### `docker-compose.yml`
- PostgreSQL service
- Django service
- Nginx service
- Volume definitions
- Environment variables

#### `Procfile`
```
web: gunicorn candyverse.wsgi:application
```

---

## 👥 User Management

### User Registration Flow

1. User visits `/register/`
2. Fills registration form
3. Form validates (email, password strength)
4. User created in database
5. Welcome email sent
6. Redirected to login page

### User Authentication

- Django built-in authentication system
- Session-based by default
- Password hashing with PBKDF2
- CSRF protection on forms

### User Profile

- Avatar upload
- Bio/biography
- Statistics tracking
- Account settings

### Password Management

- Secure password reset via email
- Token-based reset link
- Password requirements enforced
- Session invalidation on logout

---

## 🎯 Game Mechanics

### How Games Work

1. **Game Selection**: User selects a game from available list
2. **Game Start**: Game initializes with clean state
3. **Playing**: User interacts with game (based on game type)
4. **Scoring**: Points awarded based on performance
5. **Completion**: Game ends when conditions met
6. **Score Submission**: Score saved to database
7. **Leaderboard Update**: Automatically refreshed

### Scoring System

- Points based on performance
- Bonuses for speed, accuracy, difficulty
- Multipliers for streaks
- Penalties for mistakes (varies by game)

### Game Types

Examples (customize as needed):
- **Memory Game**: Match cards quickly
- **Candy Crusher**: Match 3+ candies
- **Marble Match**: Align colors
- **Spin & Win**: Spinning wheel game
- **Quick Draw**: Draw and identify candies

---

## 🏆 Leaderboard System

### Ranking Calculation

```
Rank = Position when users sorted by total_points DESC
```

### Leaderboard Types

1. **Global Leaderboard**: All-time points
2. **Weekly Leaderboard**: Points earned this week
3. **Monthly Leaderboard**: Points earned this month
4. **Game-Specific**: Top scores per game
5. **Personal**: User's own statistics

### Leaderboard Updates

- Real-time ranking updates
- Scheduled recalculation (hourly)
- Caching for performance
- Historical tracking

### Rankings Query

```python
# Top 10 users by points
top_users = LeaderboardEntry.objects.all().order_by('-total_points')[:10]
```

---

## 🔧 Development Workflow

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-game

# Make changes
git add .

# Commit with message
git commit -m "feat: Add new candy crush game"

# Push to repository
git push origin feature/new-game

# Create Pull Request on GitHub
```

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Check imports
isort .

# Security check
bandit -r .
```

### Database Migrations

```bash
# Create migration after model change
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate app_name 0002
```

### Static Files

```bash
# Collect static files
python manage.py collectstatic

# Clear collected statics
python manage.py collectstatic --clear

# Check for missing statics
python manage.py collectstatic --check
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **ModuleNotFoundError: No module named 'django'**
```bash
# Solution: Activate virtual environment and install dependencies
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### 2. **Database locked error (SQLite)**
```bash
# Solution: Close other connections, or use PostgreSQL for production
# For development:
rm db.sqlite3
python manage.py migrate
```

#### 3. **Static files not loading**
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput
```

#### 4. **Port 8000 already in use**
```bash
# Windows: Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

#### 5. **Secret key error in production**
```bash
# Solution: Set SECRET_KEY in environment variables
# In .env file
SECRET_KEY=generate-long-random-string-here
```

#### 6. **Email not sending**
```bash
# Check email settings in settings.py
# Add to settings.py for development:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### 7. **CSRF token missing**
```bash
# Ensure {% csrf_token %} is in all POST forms
# In template:
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### Performance Optimization

```python
# Use select_related for ForeignKey
games = Game.objects.select_related('user')

# Use prefetch_related for ManyToMany/reverse ForeignKey
users = User.objects.prefetch_related('gamescores')

# Use only() to limit fields
users = User.objects.only('id', 'username', 'email')

# Cache frequent queries
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutes
def leaderboard_view(request):
    pass
```

### Debugging

```bash
# Django Debug Toolbar (development only)
pip install django-debug-toolbar

# Print SQL queries
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # your code
    print(context.captured_queries)
```

---

## 📚 Additional Resources

### Documentation
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

### Deployment Guides
- [Railway Deployment](https://docs.railway.app/)
- [Render Deployment](https://render.com/docs/)
- [AWS Deployment](https://docs.aws.amazon.com/)

### Learning Resources
- [Real Python Django Tutorials](https://realpython.com/tutorials/django/)
- [Django for Beginners](https://djangoforbeginners.com/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

## 🎯 Next Steps

### Phase 1 (Current)
- ✅ Project structure
- ✅ User authentication
- ✅ Basic game system
- ✅ Leaderboard display

### Phase 2 (Upcoming)
- Add more games
- Implement achievements
- Add social features
- Mobile app development

### Phase 3 (Future)
- Real-time multiplayer
- In-game currency system
- Premium features
- Advanced analytics

---

## 📞 Support & Contact

**Questions?** Check the troubleshooting section or consult:
- GitHub Issues: Report bugs
- Documentation: Full guides
- Community Forums: Get help

**Last Updated**: May 17, 2026  
**Maintained By**: CandyVerse Team  
**License**: MIT

---

**Happy Gaming! 🍭🎮**

