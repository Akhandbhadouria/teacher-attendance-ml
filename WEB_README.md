# 🌐 Face Attendance System - Web Application

A beautiful Django web application for managing face-based attendance with real-time recognition.

## ✨ Features

- **📊 Dashboard** - Overview of attendance statistics
- **📝 User Registration** - Register users via webcam with face capture
- **✅ Mark Attendance** - Real-time face recognition and attendance marking
- **👥 User Management** - View all registered users with profiles
- **📈 Statistics** - Attendance trends and analytics
- **🎨 Modern UI** - Beautiful gradient design with smooth animations

## 🚀 Quick Start

### 1. Start the Django Server

```bash
python manage.py runserver
```

### 2. Open Your Browser

Navigate to: **http://127.0.0.1:8000/**

### 3. Use the System

- **Dashboard** - View statistics and quick actions
- **Register** - Register new users with webcam
- **Mark Attendance** - Start the camera and mark attendance automatically
- **Users** - View all registered users
- **Attendance** - View attendance records by date
- **Statistics** - View attendance trends

## 📱 Pages Overview

### Dashboard (/)
- Total users count
- Present/Absent today
- Quick action buttons
- System features overview

### Register User (/register/)
- User information form
- Live webcam capture
- Face detection and registration
- Instant feedback

### Mark Attendance (/mark-attendance/)
- Real-time webcam feed
- Automatic face detection
- Multi-face recognition
- Live attendance updates
- Statistics display

### Users List (/users/)
- Grid view of all users
- User avatars
- Contact information
- Quick access to details

### Attendance Records (/attendance/)
- Date-based filtering
- Attendance table
- Present count
- Export-ready format

### User Details (/users/<user_id>/)
- User profile
- Attendance history
- Total days present
- Complete record

### Statistics (/statistics/)
- Overall statistics
- 7-day attendance trend
- Percentage calculations
- Visual analytics

## 🎨 Design Features

### Modern UI Elements
- **Gradient Backgrounds** - Beautiful purple gradient theme
- **Glassmorphism** - Frosted glass effect on navbar
- **Smooth Animations** - Hover effects and transitions
- **Responsive Design** - Works on all screen sizes
- **Card Layouts** - Clean, organized content blocks

### Color Scheme
- Primary: #6366f1 (Indigo)
- Secondary: #8b5cf6 (Purple)
- Success: #10b981 (Green)
- Danger: #ef4444 (Red)
- Background: Purple gradient

## 🔧 Technical Details

### Backend
- **Framework**: Django 4.2.7
- **Face Recognition**: OpenCV with LBPH
- **Database**: JSON files (users.json, attendance.json)
- **Image Processing**: OpenCV, NumPy

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients
- **JavaScript** - Webcam access and AJAX
- **MediaDevices API** - Camera access

### Data Flow

```
User Registration:
Browser → Webcam → Canvas → Base64 → Django View → Face System → Database

Attendance Marking:
Browser → Webcam → Canvas → Base64 → Django View → Face Recognition → Database → Response
```

## 📊 API Endpoints

### POST /register/submit/
Register a new user with face data
- **Input**: JSON with user_id, name, email, phone, image (base64)
- **Output**: JSON with success status and message

### POST /mark-attendance/process/
Process webcam frame for attendance
- **Input**: JSON with image (base64)
- **Output**: JSON with detected faces and attendance status

## 🎯 Usage Tips

### For Best Results:

1. **Registration**
   - Use good lighting
   - Face the camera directly
   - Remove glasses/hat if possible
   - Capture when face is clearly visible

2. **Attendance Marking**
   - Stand 1-3 feet from camera
   - Look at the camera
   - Wait for detection (2-3 seconds)
   - Multiple people can be detected together

3. **Browser Compatibility**
   - Chrome (recommended)
   - Firefox
   - Safari
   - Edge

## 🔒 Security Notes

- Face encodings are one-way (cannot reconstruct face)
- Local storage only
- No external API calls
- CSRF protection enabled
- Secure file handling

## 📝 Data Storage

All data is stored in the `data/` directory:

```
data/
├── encodings/          # Face recognition data
│   ├── names.pkl
│   └── samples.pkl
├── models/             # Trained models
│   └── face_recognizer.yml
├── images/             # User photos
│   └── *.jpg
├── users.json          # User information
└── attendance.json     # Attendance records
```

## 🚀 Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up proper static file serving
4. Use a production database (PostgreSQL/MySQL)
5. Enable HTTPS
6. Configure proper media file storage

## 🎉 You're All Set!

Your web-based face attendance system is ready! Open your browser and start using it.

**Happy Tracking! 🚀**

---

**Made with ❤️ using Django, OpenCV, and modern web technologies**
