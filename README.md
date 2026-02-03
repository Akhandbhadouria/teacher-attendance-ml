# 🎓 College Face Attendance System

A secure, real-time face recognition attendance management portal designed for Colleges and Educational Institutions.

## ✨ Features

- **🔐 College Admin Portal** - Secure access for Management/Owners
- **👩‍🏫 Faculty Management** - Manage teacher records and profiles
- **📊 Real-time Dashboard** - Monitor faculty presence instantly
- **✅ Kiosk Mode** - Dedicated public interface for attendance marking
- **📈 Advanced Analytics** - Track attendance trends and reliability
- **🚀 Instant Recognition** - Fast face detection using OpenCV

## 🚀 Quick Start

### 1. Start the Server
```bash
python manage.py runserver
```

### 2. Access the Portal
- **Admin Portal**: http://127.0.0.1:8000/ (Redirects to login)
- **Kiosk Mode**: http://127.0.0.1:8000/mark-attendance/

### 3. Default Credentials
- **Username**: `admin`
- **Password**: (The one you created)

## 📱 Workflow
1. **Admin** logs in to the portal.
2. **Admin** registers new Teachers via the "Add Teacher" page.
3. **Kiosk** (entrance device) is set to "Kiosk Mode".
4. **Teachers** walk in, face the camera, and get marked present.
5. **Admin** sees real-time updates on the Dashboard.

### Register a New User

1. Click **"Register"** in the navigation menu
2. Fill in the user details:
   - User ID (unique identifier, e.g., "emp001")
   - Full Name
   - Email (optional)
   - Phone (optional)
3. Click **"Start Camera"**
4. Position your face in the center of the frame
5. Click **"Capture Face"** when ready
6. Click **"Register User"** to complete registration

### Mark Attendance

1. Click **"Mark Attendance"** in the navigation menu
2. Click **"Start Attendance System"**
3. Allow camera access when prompted
4. Stand in front of the camera
5. The system will automatically:
   - Detect your face
   - Recognize you
   - Mark your attendance
   - Show confirmation
6. **Multiple people can be detected simultaneously!**
7. Click **"Stop"** when done

### View Records

- **Users Page**: See all registered users with their photos and details
- **Attendance Page**: Filter attendance by date
- **User Details**: Click on any user to see their attendance history
- **Statistics**: View 7-day attendance trends

## 🎨 Design Features

### Modern UI Elements
- **Purple Gradient Background** - Eye-catching design
- **Glassmorphism** - Frosted glass effect on navigation
- **Smooth Animations** - Hover effects and transitions
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Card Layouts** - Clean, organized content

### Color Scheme
- Primary: Indigo (#6366f1)
- Secondary: Purple (#8b5cf6)
- Success: Green (#10b981)
- Danger: Red (#ef4444)
- Background: Purple gradient

## 🔧 Technical Stack

### Backend
- **Django 4.2.7** - Web framework
- **OpenCV** - Face detection and recognition
- **LBPH Algorithm** - Face recognition
- **NumPy** - Numerical operations
- **JSON Database** - Simple data storage

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients
- **JavaScript (ES6+)** - Webcam and AJAX
- **MediaDevices API** - Camera access

## 📁 Project Structure

```
dig_attendence/
├── attendance/                 # Django app
│   ├── templates/             # HTML templates
│   │   └── attendance/
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── register.html
│   │       ├── mark_attendance.html
│   │       ├── users.html
│   │       ├── attendance.html
│   │       ├── user_detail.html
│   │       └── statistics.html
│   ├── views.py               # View logic
│   └── urls.py                # URL routing
├── attendance_web/            # Django project
│   ├── settings.py
│   └── urls.py
├── static/
│   └── css/
│       └── style.css          # Modern CSS
├── src/                       # Core modules
│   ├── database.py            # Database management
│   ├── simple_face_recognition.py  # Face recognition
│   ├── main.py                # CLI interface
│   ├── register_user_simple.py
│   ├── mark_attendance_simple.py
│   └── view_attendance.py
├── data/                      # Data storage
│   ├── encodings/             # Face data
│   ├── models/                # Trained models
│   ├── images/                # User photos
│   ├── users.json             # User info
│   └── attendance.json        # Attendance records
├── manage.py                  # Django management
├── requirements_web.txt       # Dependencies
└── README.md                  # This file
```

## 🎯 Features in Detail

### 1. Dashboard
- Total users count
- Present/Absent today statistics
- Quick action buttons
- Feature highlights
- Today's date display

### 2. User Registration
- Form validation
- Live webcam preview
- Real-time face detection feedback
- Automatic face encoding
- Image storage
- Success/error messages

### 3. Mark Attendance
- Real-time webcam feed
- Automatic face detection (every 2 seconds)
- Multi-face recognition
- Live attendance updates
- Visual feedback for detected faces
- Confidence scores
- Attendance status display

### 4. User Management
- Grid view of all users
- User avatars/photos
- Contact information
- Registration date
- Individual user details
- Attendance history per user

### 5. Attendance Records
- Date-based filtering
- Tabular view
- Present count
- Sortable columns
- Export-ready format

### 6. Statistics
- Overall statistics
- 7-day attendance trend
- Percentage calculations
- Visual analytics

## 💡 Usage Tips

### For Best Results:

**During Registration:**
- ✅ Use good lighting
- ✅ Face the camera directly
- ✅ Remove glasses/hat if possible
- ✅ Keep a neutral expression
- ✅ Ensure face is clearly visible

**During Attendance:**
- ✅ Stand 1-3 feet from camera
- ✅ Look at the camera
- ✅ Wait 2-3 seconds for detection
- ✅ Multiple people can stand together
- ✅ Maintain similar lighting as registration

**Browser Compatibility:**
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## 🔒 Security & Privacy

- Face encodings are one-way (cannot reconstruct face)
- Local storage only (no cloud)
- No external API calls
- CSRF protection enabled
- Secure file handling
- Privacy-friendly design

## 📊 Data Storage

All data is stored locally in a SQLite database (`db.sqlite3`):

**Users Table**:
- User ID (Primary Key)
- Name
- Email
- Phone
- Registration Date

**Attendance Table**:
- ID (Primary Key)
- User (Foreign Key)
- Date
- Time
- Timestamp

## 🔒 Administration

Access the Django Admin Panel to manage users and attendance:

1. Go to: **http://127.0.0.1:8000/admin/**
2. Login with superuser credentials
3. View, edit, or delete records

## 🛠️ Troubleshooting

### Camera Not Working
- **Issue**: Camera access denied
- **Solution**: Allow camera permissions in browser settings

### Face Not Detected
- **Issue**: No face detected during registration/attendance
- **Solution**: 
  - Improve lighting
  - Move closer to camera
  - Ensure face is clearly visible
  - Remove obstructions

### Wrong Person Recognized
- **Issue**: System recognizes wrong person
- **Solution**:
  - Re-register with better quality image
  - Ensure good lighting
  - Check if multiple similar faces exist

### Server Not Starting
- **Issue**: Django server won't start
- **Solution**:
  ```bash
  cd /Users/lambardaar/Downloads/dig_attendence
  python manage.py runserver
  ```

### Page Not Loading
- **Issue**: 404 or blank page
- **Solution**:
  - Ensure server is running
  - Check URL: http://127.0.0.1:8000/
  - Clear browser cache

## 🚀 Advanced Features

### API Endpoints

**POST /register/submit/**
- Register new user
- Input: JSON with user_id, name, email, phone, image (base64)
- Output: Success status and message

**POST /mark-attendance/process/**
- Process webcam frame
- Input: JSON with image (base64)
- Output: Detected faces and attendance status

This provides:
- Text-based menu
- User registration
- Attendance marking
- View records

### API Endpoints

**POST /register/submit/**
- Register new user
- Input: JSON with user_id, name, email, phone, image (base64)
- Output: Success status and message

**POST /mark-attendance/process/**
- Process webcam frame
- Input: JSON with image (base64)
- Output: Detected faces and attendance status

## 📝 Development

### Requirements

Install dependencies:
```bash
pip install -r requirements_web.txt
```

### Database Migrations

```bash
python manage.py migrate
```

### Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

## 🎉 You're All Set!

Your face attendance system is fully functional and ready to use!

**Access the web interface at: http://127.0.0.1:8000/**

### Current Status:
- ✅ 1 user registered (irfan, ID: 12317691)
- ✅ Web interface running
- ✅ Face recognition working
- ✅ Database initialized
- ✅ All features operational

---

**Made with ❤️ using Django, OpenCV, and modern web technologies**

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the console/terminal for error messages
3. Ensure all dependencies are installed
4. Verify camera permissions

**Happy Tracking! 🚀**
