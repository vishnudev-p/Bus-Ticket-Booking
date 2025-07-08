#!/bin/bash

# Bus Ticket App Deployment Script
# This script helps prepare your app for deployment

echo "🚀 Bus Ticket App Deployment Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "backend/manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📋 Checking prerequisites..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository found"
fi

# Check backend requirements
if [ -f "backend/requirements.txt" ]; then
    echo "✅ Backend requirements found"
else
    echo "❌ Backend requirements.txt not found"
    exit 1
fi

# Check frontend package.json
if [ -f "frontend/busticket-frontend/package.json" ]; then
    echo "✅ Frontend package.json found"
else
    echo "❌ Frontend package.json not found"
    exit 1
fi

echo ""
echo "🔧 Setting up environment files..."

# Create backend .env template
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend .env template..."
    cat > backend/.env << EOF
# Backend Environment Variables
SECRET_KEY=your-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
EOF
    echo "✅ Backend .env template created"
else
    echo "✅ Backend .env already exists"
fi

# Create frontend .env template
if [ ! -f "frontend/busticket-frontend/.env" ]; then
    echo "📝 Creating frontend .env template..."
    cat > frontend/busticket-frontend/.env << EOF
# Frontend Environment Variables
REACT_APP_API_URL=https://your-backend-domain.com
EOF
    echo "✅ Frontend .env template created"
else
    echo "✅ Frontend .env already exists"
fi

echo ""
echo "🔧 Installing dependencies..."

# Install backend dependencies
echo "📦 Installing Python dependencies..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Please create one:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
fi

pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Install frontend dependencies
echo "📦 Installing Node.js dependencies..."
cd ../frontend/busticket-frontend
npm install
echo "✅ Frontend dependencies installed"

echo ""
echo "🔧 Building frontend..."
npm run build
echo "✅ Frontend built successfully"

echo ""
echo "🔧 Collecting static files..."
cd ../../backend
python manage.py collectstatic --noinput
echo "✅ Static files collected"

echo ""
echo "🔧 Running migrations..."
python manage.py migrate
echo "✅ Migrations completed"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update the .env files with your actual values"
echo "2. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Prepare for deployment'"
echo "   git push origin main"
echo "3. Choose a hosting platform (see DEPLOYMENT_GUIDE.md)"
echo "4. Set up environment variables on your hosting platform"
echo "5. Deploy!"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md" 