# Deploying to Vercel

## Prerequisites
- A GitHub account
- A Vercel account (sign up at vercel.com with your GitHub)
- Your project pushed to a GitHub repository

## Step-by-Step Deployment Guide

### 1. Prepare Environment Variables
Before deploying, you need to set up environment variables in Vercel:
- `SECRET_KEY`: Your Django secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Will be automatically set to `.vercel.app` domains
- `CSRF_TRUSTED_ORIGINS`: Should include `https://your-app.vercel.app`

### 2. Important: Preprocessed Data
⚠️ **CRITICAL**: The `preprocessed_data.pkl` file is ignored by git (it's too large). You have two options:

**Option A (Recommended)**: Build during deployment
- The `build_files.sh` script will automatically run `preprocess_data.py` during build
- This happens automatically with the current configuration

**Option B**: Upload manually
- If build fails, you may need to reduce the CSV file size or optimize preprocessing
- Consider storing the pickle file externally (AWS S3, etc.) and loading it from there

### 3. Push to GitHub
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 4. Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and log in with GitHub
2. Click "Add New Project"
3. Import your movie recommendation repository
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: bash build_files.sh
   - **Output Directory**: Leave empty

5. Add Environment Variables:
   - Go to "Environment Variables" section
   - Add the following:
     ```
     SECRET_KEY=<your-django-secret-key>
     DEBUG=False
     ALLOWED_HOSTS=.vercel.app
     CSRF_TRUSTED_ORIGINS=https://*.vercel.app
     ```

6. Click "Deploy"

### 5. Post-Deployment

After successful deployment:
1. Visit your app at: `https://your-project-name.vercel.app`
2. Test the movie search functionality
3. Check that static files (CSS, images) are loading correctly

### Troubleshooting

**Build fails due to memory/size limits:**
- Vercel has a 250MB deployment size limit
- The preprocessed data might be too large
- Solution: Host the pickle file externally or reduce dataset size

**Static files not loading:**
- Run `vercel --prod` again
- Check that `collectstatic` ran successfully in build logs

**500 Internal Server Error:**
- Check Vercel logs: `vercel logs <deployment-url>`
- Verify environment variables are set correctly
- Ensure `ALLOWED_HOSTS` includes your Vercel domain

**Database issues:**
- SQLite is read-only on Vercel
- For admin/authentication features, consider using PostgreSQL via Vercel Postgres
- Your current app doesn't use database for main functionality, so this should be fine

### Important Notes

1. **Serverless Limitations**: 
   - Each request runs in a serverless function
   - Cold starts may cause initial delays
   - The pickle file loads on each function invocation

2. **Performance Optimization**:
   - Consider using a CDN for static files
   - Cache the preprocessed data if possible
   - Optimize the similarity computation

3. **Scaling**:
   - Vercel has request/execution time limits
   - For high traffic, consider alternatives like Railway, Render, or AWS

### Local Testing

Before deploying, test locally:
```bash
# Set environment variables
cp .env.example .env
# Edit .env with your values

# Run the build script
bash build_files.sh

# Test the server
python manage.py runserver
```

### Updating Your Deployment

To update your app:
```bash
git add .
git commit -m "Update description"
git push origin main
```

Vercel will automatically redeploy on every push to main branch.

## Additional Resources
- [Vercel Documentation](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
