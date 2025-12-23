# Deployment Guide

## Automated Preprocessing Setup

Your app is now configured to automatically generate the similarity data file during deployment.

### Files Created:
- `recommendation/preprocess_data.py` - Preprocessing script
- `build.sh` - Build script for deployment platforms
- Auto-generation fallback in `similarity.py`

---

## Deployment Instructions

### **Option 1: Render.com (Recommended)**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add deployment preprocessing"
   git push
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com) and sign up
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command:** `./build.sh`
     - **Start Command:** `gunicorn movie.wsgi:application`
     - **Environment Variables:**
       - `SECRET_KEY` = (generate a new random key)
       - `DEBUG` = `False`
       - `ALLOWED_HOSTS` = `your-app-name.onrender.com`
       - `PYTHON_VERSION` = `3.11.0`

3. **Deploy!** Render will:
   - Install dependencies
   - Run preprocessing (generates pkl file)
   - Start your app

---

### **Option 2: Railway.app**

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Create new project from GitHub
4. Add build command: `./build.sh`
5. Set environment variables (same as above)

---

### **Option 3: PythonAnywhere**

1. Upload files via Git or file manager
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. **Run preprocessing manually once:**
   ```bash
   python recommendation/preprocess_data.py
   ```
5. Configure WSGI file

---

## Environment Variables for Production

Set these on your deployment platform:

```
SECRET_KEY=<generate-new-random-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**Generate a new SECRET_KEY:** Run in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## What Happens During Deployment:

1. Platform pulls your code
2. Runs `build.sh`:
   - Installs dependencies
   - Collects static files
   - **Generates preprocessed_data.pkl from CSV** (one time, ~2-5 minutes)
3. Starts your app
4. Users can access your site!

The pkl file is generated ONCE during build and reused for all visitors.

---

## Testing Locally

To test preprocessing locally:
```bash
python recommendation/preprocess_data.py
```

This generates the pkl file so you can run your app locally.
