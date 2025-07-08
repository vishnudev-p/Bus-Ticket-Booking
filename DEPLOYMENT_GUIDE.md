# 🚀 Bus Ticket App Deployment Guide

This guide will help you deploy your Bus Ticket App (Django + React) to various hosting platforms.

## 📋 Prerequisites

1. **GitHub Account** - Push your code to GitHub
2. **Environment Variables** - Set up production environment variables
3. **Database** - Choose between SQLite (development) or PostgreSQL (production)

## 🔧 Pre-deployment Setup

### 1. Update Frontend API Configuration

All frontend components now use environment variables for API URLs. Create a `.env` file in the frontend directory:

```bash
# frontend/busticket-frontend/.env
REACT_APP_API_URL=https://your-backend-domain.com
```

### 2. Environment Variables for Backend

Create a `.env` file in the backend directory:

```bash
# backend/.env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🚀 Deployment Options

### Option 1: Railway (Recommended for Beginners)

**Pros:** Easy deployment, free tier, automatic HTTPS, database included

#### Steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy Backend:**
   - Go to [Railway](https://railway.app)
   - Connect your GitHub account
   - Create new project → Deploy from GitHub repo
   - Select the `backend` folder
   - Add environment variables in Railway dashboard
   - Railway will auto-detect Django and deploy

3. **Deploy Frontend:**
   - Create another Railway project
   - Select the `frontend/busticket-frontend` folder
   - Add build command: `npm run build`
   - Add start command: `serve -s build`
   - Add environment variable: `REACT_APP_API_URL=https://your-backend-railway-url`

### Option 2: Render

**Pros:** Free tier, easy deployment, PostgreSQL included

#### Steps:

1. **Backend Deployment:**
   - Go to [Render](https://render.com)
   - Create new Web Service
   - Connect GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn busticket.wsgi:application`
   - Add environment variables

2. **Frontend Deployment:**
   - Create new Static Site
   - Build Command: `npm run build`
   - Publish Directory: `build`
   - Add environment variables

### Option 3: Vercel (Frontend) + Railway (Backend)

**Pros:** Best performance for React, easy deployment

#### Steps:

1. **Deploy Backend to Railway** (see Option 1)

2. **Deploy Frontend to Vercel:**
   - Go to [Vercel](https://vercel.com)
   - Import GitHub repo
   - Set root directory to `frontend/busticket-frontend`
   - Add environment variable: `REACT_APP_API_URL=https://your-backend-url`
   - Deploy

### Option 4: Heroku

**Pros:** Mature platform, good documentation

#### Steps:

1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy Backend:**
   ```bash
   cd backend
   heroku create your-app-name
   heroku addons:create heroku-postgresql:mini
   git push heroku main
   ```

3. **Deploy Frontend:**
   ```bash
   cd frontend/busticket-frontend
   heroku create your-frontend-name
   heroku buildpacks:set mars/create-react-app
   git push heroku main
   ```

## 🔧 Manual Deployment Steps

### 1. Update All Frontend Components

You need to update all components to use the centralized API configuration. Here's a script to do it:

```bash
# Run this in the frontend directory
find src/components -name "*.js" -exec sed -i 's|http://127.0.0.1:8000|${API_URL}|g' {} \;
```

### 2. Build Frontend

```bash
cd frontend/busticket-frontend
npm install
npm run build
```

### 3. Collect Static Files (Backend)

```bash
cd backend
python manage.py collectstatic --noinput
```

### 4. Run Migrations

```bash
cd backend
python manage.py migrate
```

## 🌐 Domain Configuration

### Custom Domain Setup

1. **Buy a domain** (Namecheap, GoDaddy, etc.)
2. **Configure DNS** to point to your hosting provider
3. **Update environment variables** with your domain
4. **Set up SSL certificates** (automatic with most platforms)

### Environment Variables for Production

```bash
# Backend (.env)
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,api.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
DATABASE_URL=postgresql://user:password@host:port/database

# Frontend (.env)
REACT_APP_API_URL=https://api.your-domain.com
```

## 🔒 Security Checklist

- [ ] Change Django SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up CORS properly
- [ ] Use HTTPS everywhere
- [ ] Set up proper database (PostgreSQL)
- [ ] Configure static files serving
- [ ] Set up proper logging

## 🐛 Troubleshooting

### Common Issues:

1. **CORS Errors:**
   - Check CORS_ALLOWED_ORIGINS in backend settings
   - Ensure frontend URL is included

2. **Database Connection:**
   - Verify DATABASE_URL format
   - Check database credentials

3. **Static Files Not Loading:**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT configuration

4. **Build Failures:**
   - Check Node.js version compatibility
   - Verify all dependencies are installed

## 📞 Support

If you encounter issues:

1. Check the hosting platform's logs
2. Verify environment variables are set correctly
3. Test locally with production settings
4. Check the platform's documentation

## 🎉 Success!

Once deployed, your Bus Ticket App will be accessible at:
- Frontend: `https://your-frontend-domain.com`
- Backend API: `https://your-backend-domain.com`

Remember to update the frontend's `REACT_APP_API_URL` to point to your backend URL! 