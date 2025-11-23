# Frontend Options for Multi-Agent Tourism System

This directory contains three different frontend implementations for the Multi-Agent Tourism System. Choose the one that best fits your needs!

## 🌐 Option 1: HTML/CSS/JavaScript (Recommended for Quick Start)

**File**: `index.html`

### Features:
- ✅ No dependencies or build process required
- ✅ Modern, responsive design
- ✅ Real-time API status checking
- ✅ Example queries for easy testing
- ✅ Beautiful gradient design
- ✅ Error handling and loading states

### How to Run:
```bash
# 1. Start the backend API first
cd api
python main.py

# 2. Open the HTML file in your browser
# Option A: Double-click frontend/index.html
# Option B: Use a local server (recommended)
cd frontend
python -m http.server 8080
# Then visit: http://localhost:8080
```

### Screenshots:
- Clean, modern interface
- Real-time API status indicator
- Clickable example queries
- Formatted response display

---

## 🚀 Option 2: Streamlit (Recommended for Python Developers)

**File**: `streamlit_app.py`

### Features:
- ✅ Python-based web app
- ✅ Auto-refreshing components
- ✅ Sidebar with system information
- ✅ Built-in example queries
- ✅ Excellent for demos and prototyping
- ✅ Minimal setup required

### How to Run:
```bash
# 1. Install Streamlit
pip install streamlit

# 2. Start the backend API
cd api
python main.py

# 3. Run the Streamlit app (in another terminal)
cd frontend
streamlit run streamlit_app.py
```

### Access:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000

---

## ⚛️ Option 3: React (Recommended for Production)

**Directory**: `react_app/`

### Features:
- ✅ Modern React with hooks
- ✅ Styled Components for styling
- ✅ Responsive design
- ✅ Professional UI/UX
- ✅ Component-based architecture
- ✅ Production-ready build system

### How to Run:
```bash
# 1. Start the backend API first
cd api
python main.py

# 2. Install React dependencies
cd frontend/react_app
npm install

# 3. Start the React development server
npm start
```

### Access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Build for Production:
```bash
cd frontend/react_app
npm run build
```

---

## 🎯 Which Frontend Should You Choose?

### **HTML/CSS/JS** - Best for:
- ✅ Quick demos and testing
- ✅ No build process needed
- ✅ Simple deployment (just upload files)
- ✅ Learning and education purposes

### **Streamlit** - Best for:
- ✅ Python developers
- ✅ Data science presentations
- ✅ Internal tools and dashboards
- ✅ Rapid prototyping

### **React** - Best for:
- ✅ Production applications
- ✅ Professional presentations
- ✅ Scalable frontend development
- ✅ Team development with frontend specialists

---

## 🔧 Common Setup Steps

### 1. Start the Backend API
```bash
# From project root
cd api
python main.py
```
**Verify**: Visit http://localhost:8000/docs to see API documentation

### 2. Update API URL (if needed)
If your backend runs on a different port, update the API_BASE_URL in:
- HTML: Line 170 in `index.html`
- Streamlit: Line 25 in `streamlit_app.py`  
- React: Line 87 in `TourismAssistant.js`

### 3. Test the Connection
All frontends include API status indicators that show:
- 🟢 Green: API is online and ready
- 🔴 Red: API is offline or unreachable

---

## 🎨 Customization

### Colors and Styling:
- **HTML**: Modify CSS variables in `<style>` section
- **Streamlit**: Edit custom CSS in `st.markdown()`
- **React**: Update styled-components or add CSS files

### Adding Features:
- Query history
- Favorites/bookmarks
- Map integration
- Weather charts
- User preferences

---

## 🐛 Troubleshooting

### Common Issues:

1. **"API is offline"**
   - Make sure backend is running on port 8000
   - Check if you can access http://localhost:8000/health

2. **CORS errors (React)**
   - Backend already has CORS enabled
   - Make sure both frontend and backend are running

3. **Port conflicts**
   - HTML: Use different port with `python -m http.server 8080`
   - Streamlit: Use `streamlit run app.py --server.port 8502`
   - React: Use `PORT=3001 npm start`

4. **Network errors**
   - Check if backend is accessible
   - Verify API_BASE_URL matches your backend URL

---

## 📱 Mobile Responsiveness

All frontends are mobile-responsive:
- ✅ Touch-friendly buttons
- ✅ Responsive layouts
- ✅ Readable fonts on small screens
- ✅ Optimized for mobile browsers

---

## 🚀 Deployment Options

### HTML Frontend:
- Upload to any web server
- GitHub Pages
- Netlify/Vercel (static hosting)

### Streamlit:
- Streamlit Cloud
- Heroku
- Google Cloud Run

### React:
- Vercel/Netlify
- AWS S3 + CloudFront
- GitHub Pages (after `npm run build`)

---

## 🔗 Integration with Backend

All frontends communicate with the same REST API:

### Main Endpoint:
```
POST /query
Content-Type: application/json

{
  "query": "I'm going to Paris, what's the weather?"
}
```

### Response Format:
```json
{
  "response": "In Paris it's currently 18°C with a chance of 20% to rain.",
  "place_name": "Paris"
}
```

### Health Check:
```
GET /health

{
  "status": "healthy",
  "service": "tourism-agent"
}
```

---

Choose your preferred frontend and start exploring the world with AI! 🌍✨