# CandyVerse - Hosting, Deployment & Maintenance Guide

## 📋 Table of Contents
1. [Hosting Options](#hosting-options)
2. [Free Tier Options](#free-tier-options)
3. [Data Storage & Long-term Memory](#data-storage--long-term-memory)
4. [Maintenance Schedule](#maintenance-schedule)
5. [Deployment Instructions](#deployment-instructions)
6. [Monitoring & Support](#monitoring--support)

---

## 🌐 Hosting Options

### 1. **Railway.app** (Recommended for Free Start)
- **Cost**: Free tier includes $5 credit/month
- **Database**: PostgreSQL, MySQL, SQLite supported
- **Setup**: Simple GitHub integration
- **Pros**: Easy deployment, good free tier, auto-scaling
- **Cons**: Credits run out after free tier
- **Link**: https://railway.app

#### Deployment Steps:
```bash
# 1. Connect GitHub repository
# 2. Select Python as environment
# 3. Add PostgreSQL plugin
# 4. Set environment variables
# 5. Deploy
```

---

### 2. **Render.com** (Free Tier Available)
- **Cost**: Free tier, paid plans from $7/month
- **Database**: PostgreSQL included
- **Setup**: GitHub push-to-deploy
- **Pros**: Free tier available, auto-deploy on push
- **Cons**: Spins down free tier after 15 minutes of inactivity
- **Link**: https://render.com

#### Deployment Steps:
```bash
# 1. Create new Web Service
# 2. Connect GitHub repo
# 3. Set build command: pip install -r requirements.txt
# 4. Set start command: gunicorn candyverse.wsgi
# 5. Add PostgreSQL database
# 6. Deploy
```

---

### 3. **PythonAnywhere** (Beginner Friendly)
- **Cost**: Free tier available, paid from $5/month
- **Database**: MySQL included
- **Setup**: Direct file upload or Git integration
- **Pros**: Easy for beginners, simple setup
- **Cons**: Limited resources on free tier
- **Link**: https://www.pythonanywhere.com

#### Deployment Steps:
```bash
# 1. Create account and select Python 3.9
# 2. Upload code or clone from Git
# 3. Create web app (Django)
# 4. Configure virtual environment
# 5. Set WSGI file
```

---

### 4. **AWS (EC2 + RDS)**
- **Cost**: Free tier (12 months), then ~$10-30/month
- **Database**: RDS PostgreSQL/MySQL
- **Setup**: More complex, requires configuration
- **Pros**: Scalable, reliable, large free tier
- **Cons**: Complex setup, potential unexpected costs
- **Link**: https://aws.amazon.com

#### Deployment Steps:
```bash
# 1. Launch EC2 instance (Ubuntu 20.04+)
# 2. SSH into instance
# 3. Install Python, pip, PostgreSQL client
# 4. Clone repository
# 5. Create virtual environment and install dependencies
# 6. Set up RDS PostgreSQL database
# 7. Configure gunicorn + nginx
```

---

### 5. **DigitalOcean (App Platform)**
- **Cost**: Free tier trial, then $5+/month
- **Database**: Managed databases available
- **Setup**: GitHub integration
- **Pros**: Developer-friendly, good pricing
- **Cons**: Limited free tier
- **Link**: https://www.digitalocean.com

---

### 6. **Heroku** (Legacy)
- **Status**: Free tier removed as of November 2022
- **Cost**: Paid plans start at $7/month
- **Note**: Not recommended for cost-conscious deployments

---

## 💰 Free Tier Options (Recommended for Launch)

### **Best Free Option: Railway.app**
```
✅ Pros:
  - $5/month free credit (often enough for small app)
  - Simple Django deployment
  - Automatic PostgreSQL database
  - GitHub auto-deploy
  - Good documentation

⏱️ Duration: Unlimited (as long as usage within $5/month)
```

### **Best Free Option #2: Render.com**
```
✅ Pros:
  - Completely free tier
  - Auto-deploy from GitHub
  - PostgreSQL included
  - SSL certificate free

⚠️ Limitations:
  - Free tier services spin down after 15 min inactivity
  - Slower response times
```

### **Best Free Option #3: PythonAnywhere**
```
✅ Pros:
  - Free tier available
  - Simple setup, beginner-friendly
  - No credit card required
  - 100MB free disk space

⚠️ Limitations:
  - Limited CPU time (100 seconds/day)
  - Limited databases
```

---

## 💾 Data Storage & Long-term Memory

### **Database Options**

#### 1. **PostgreSQL** (Recommended)
- **Type**: Relational database
- **Best For**: Production environments
- **Backup Strategy**: Automated daily backups
- **Cost**: Free if self-hosted, $15-100/month if managed
- **Pros**: Reliable, ACID compliant, great for Django
- **Setup**:
```bash
# Install locally for testing
# Use managed service (Railway, Render, AWS RDS) for production
```

#### 2. **SQLite** (Current)
- **Type**: File-based database
- **Best For**: Development/small projects
- **Limitations**: Not suitable for production multi-user apps
- **Backup Strategy**: Copy db.sqlite3 file regularly

#### 3. **MySQL** (Alternative)
- **Type**: Relational database
- **Cost**: Free if self-hosted, $15+/month if managed
- **Pros**: Popular, good for web apps
- **Cons**: Less powerful than PostgreSQL

### **Backup Strategy**

#### Automated Backups:
```bash
# Schedule daily database backups
# Use managed service backup features (Railway, Render auto-backup)
# Store backups in cloud storage (AWS S3, Google Cloud Storage)
```

#### Manual Backup Script:
```python
# Create backup_db.py
import subprocess
import datetime
import os

def backup_database():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"db_backup_{timestamp}.sql"
    
    # For PostgreSQL
    subprocess.run([
        'pg_dump',
        'your_database_name',
        '-U', 'your_username',
        '-f', backup_file
    ])
    
    print(f"Backup created: {backup_file}")

if __name__ == "__main__":
    backup_database()
```

#### Long-term Storage:
- **AWS S3**: Store backups ($0.023/GB/month)
- **Google Cloud Storage**: Store backups ($0.020/GB/month)
- **Dropbox/OneDrive**: For small databases (free tier available)

### **Data Retention Policy**
```
- Keep last 7 daily backups locally
- Keep last 4 weekly backups in cloud
- Keep last 12 monthly backups archived
- Total backup retention: 12+ months
```

---

## 🔧 Maintenance Schedule

### **Daily Tasks (Automated)**
- ✅ Database auto-backups
- ✅ Log monitoring
- ✅ Error tracking (using Sentry/Rollbar)

### **Weekly Tasks**
```
Monday:
  - Review error logs
  - Check deployment health
  - Monitor database size

Wednesday:
  - Dependency security scan
  - Review user feedback
```

### **Monthly Tasks**
```
1st of Month:
  - Update Python packages
  - Review security advisories
  - Performance analysis
  - Cost review
  
Mid-month:
  - Database cleanup (deleted user data)
  - Cache clearing
  - Log rotation
```

### **Quarterly Tasks**
```
Every 3 Months:
  - Major dependency updates
  - Security audit
  - Backup restoration test
  - Performance optimization review
```

### **Maintenance Commands**

#### Update Dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
pip freeze > requirements.txt
```

#### Django Maintenance:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py clearsessions
python manage.py check --deploy
```

#### Database Optimization:
```bash
# PostgreSQL
ANALYZE;
VACUUM;

# Django
python manage.py dbshell
```

---

## 🚀 Deployment Instructions

### **Step 1: Prepare Application**

```bash
# Update requirements.txt
pip freeze > requirements.txt

# Create Procfile (if using Heroku-like services)
# Already present in project
```

### **Step 2: Environment Variables**

Create `.env` file (DO NOT commit to git):
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host/dbname
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
DJANGO_SETTINGS_MODULE=candyverse.settings
```

### **Step 3: Static Files**

```bash
python manage.py collectstatic --noinput
```

### **Step 4: Database Migration**

```bash
python manage.py migrate
```

### **Step 5: Deploy to Railway (Quick Start)**

```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to Railway.app
# 3. Create new project
# 4. Connect GitHub repository
# 5. Select branch (main)
# 6. Railway auto-detects Django app
# 7. Add PostgreSQL plugin
# 8. Set environment variables
# 9. Deploy automatically
```

### **Step 6: Deploy to Render (Quick Start)**

```bash
# 1. Push to GitHub
# 2. Go to Render.com
# 3. Create New > Web Service
# 4. Connect GitHub
# 5. Name: candyverse
# 6. Runtime: Python 3
# 7. Build Command: pip install -r requirements.txt
# 8. Start Command: gunicorn candyverse.wsgi:application
# 9. Environment: Production
# 10. Add Environment Variables
# 11. Deploy
```

### **Custom Domain Setup**

After deployment:
```
1. Purchase domain (GoDaddy, Namecheap, etc.)
2. Point domain DNS to your host:
   - Railway: Add CNAME record
   - Render: Add CNAME record
   - AWS: Point to Load Balancer
3. Wait for DNS propagation (up to 24 hours)
4. Enable HTTPS/SSL (usually automatic)
```

---

## 📊 Monitoring & Support

### **Error Tracking**

#### Option 1: Sentry (Recommended Free)
```python
# Install in settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=False
)
```

#### Option 2: Rollbar (Free tier)
```python
# Add to settings.py
ROLLBAR = {
    'access_token': 'your-rollbar-token',
    'environment': 'production',
    'enabled': True,
}
```

### **Performance Monitoring**

#### Django Debug Toolbar (Development):
```bash
pip install django-debug-toolbar
```

#### Application Performance Monitoring (Production):
- **New Relic**: Free tier available
- **DataDog**: Free tier available
- **Scout APM**: Django-specific, free tier

### **Health Checks**

```python
# Add to urls.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat()
    })

# URL pattern
path('health/', health_check),
```

### **Logging**

```python
# Configure in settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'candyverse.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## 💡 Cost Optimization Tips

### **Reduce Hosting Costs**
- ✅ Use free tier services initially
- ✅ Auto-scale resources based on demand
- ✅ Use CDN for static files (Cloudflare free tier)
- ✅ Optimize database queries
- ✅ Cache frequently accessed data (Redis)

### **Free Tools & Services**
- **Cloudflare CDN**: Free tier for static files
- **GitHub Actions**: Free CI/CD
- **MongoDB Atlas**: Free tier (512MB)
- **Firebase**: Free tier for real-time features
- **SendGrid Email**: Free tier (100 emails/day)

### **Estimated Monthly Costs**

#### Minimal Setup (Starting Free)
```
Railway: $0-5/month (in free credit)
Total: $0-5/month ✅
```

#### Standard Production Setup
```
Railway (upgraded): $10/month
PostgreSQL Database: $15/month
Monitoring (Sentry): $0 (free tier)
Domain: $10/year (~$1/month)
CDN (Cloudflare): $0 (free tier)
--
Total: ~$26/month
```

#### Full Production Setup
```
AWS EC2 (t3.medium): $30/month
RDS PostgreSQL: $30/month
CloudFront CDN: $5/month
Route53 DNS: $0.50/month
Backup Storage: $5/month
Monitoring: $10/month
--
Total: ~$80/month
```

---

## 📝 Quick Reference

### **Recommended Free Launch Stack**
```
✅ Railway.app or Render.com for hosting
✅ PostgreSQL for database
✅ Cloudflare for CDN
✅ GitHub for version control
✅ Sentry for error tracking
✅ Let's Encrypt for SSL (automatic)
```

### **Common Deployment URLs**
- Railway: `https://candyverse-xxx.railway.app`
- Render: `https://candyverse.onrender.com`
- Custom Domain: `https://candyverse.com`

### **Emergency Procedures**

**If Production is Down:**
1. Check deployment logs (Railway/Render dashboard)
2. Verify database connection
3. Check error tracking (Sentry)
4. Roll back to previous version if needed
5. Notify users of status

**Database Recovery:**
1. Stop application
2. Restore from latest backup
3. Verify data integrity
4. Restart application

---

## 📞 Support & Resources

### **Documentation Links**
- Django Docs: https://docs.djangoproject.com
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- PostgreSQL: https://www.postgresql.org/docs

### **Community Help**
- Django Community: https://forum.djangoproject.com
- Stack Overflow: Tag `django`
- Reddit: r/django

### **Security Resources**
- OWASP Top 10: https://owasp.org/Top10
- Django Security: https://docs.djangoproject.com/en/stable/topics/security
- Dependency Scanning: https://www.sonarcloud.io

---

**Last Updated**: May 17, 2026
**Next Review**: August 17, 2026

