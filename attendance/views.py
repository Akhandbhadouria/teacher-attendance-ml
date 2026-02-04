from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from django.db.models import Count, Q
import json
import os
import sys
import cv2
from datetime import datetime, date, timedelta
import base64
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from simple_face_recognition import SimpleFaceRecognitionSystem
from .models import User, Attendance, Timetable, LectureAttendance

# Initialize face recognition system
face_system = SimpleFaceRecognitionSystem()

@login_required
def index(request):
    """College Admin Dashboard"""
    total_teachers = User.objects.count()
    today = date.today()
    present_today = Attendance.objects.filter(date=today).count()
    absent_today = total_teachers - present_today
    
    context = {
        'total_teachers': total_teachers,
        'present_today': present_today,
        'absent_today': absent_today,
        'today_date': today.strftime("%B %d, %Y")
    }
    return render(request, 'attendance/index.html', context)

@login_required
def users_list(request):
    """List all Faculty/Teachers"""
    teachers = User.objects.all()
    
    teachers_data = []
    for teacher in teachers:
        teachers_data.append({
            'user_id': teacher.user_id,
            'name': teacher.name,
            'email': teacher.email or 'N/A',
            'phone': teacher.phone or 'N/A',
            'registered_at': teacher.registered_at.strftime("%Y-%m-%d %H:%M:%S"),
            'image_path': f'/media/images/{teacher.user_id}.jpg' if os.path.exists(f'data/images/{teacher.user_id}.jpg') else None
        })
    
    context = {'teachers': teachers_data}
    return render(request, 'attendance/users.html', context)

@login_required
def attendance_records(request):
    """View teacher attendance logs"""
    selected_date = request.GET.get('date', date.today().strftime("%Y-%m-%d"))
    
    try:
        filter_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    except:
        filter_date = date.today()
    
    records = Attendance.objects.filter(date=filter_date).select_related('user')
    
    attendance_data = []
    for record in records:
        attendance_data.append({
            'user_id': record.user.user_id,
            'name': record.user.name,
            'date': record.date.strftime("%Y-%m-%d"),
            'time': record.time.strftime("%H:%M:%S"),
            'timestamp': record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    context = {
        'attendance_records': attendance_data,
        'selected_date': filter_date.strftime("%Y-%m-%d"),
        'today': date.today().strftime("%Y-%m-%d")
    }
    return render(request, 'attendance/attendance.html', context)

@login_required
def register_page(request):
    """Teacher Registration page - Admin only"""
    return render(request, 'attendance/register.html')

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def register_user(request):
    """Register a new teacher"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        name = data.get('name')
        email = data.get('email', '')
        phone = data.get('phone', '')
        password = data.get('password')
        image_data = data.get('image')
        
        if not all([user_id, name, password, image_data]):
            return JsonResponse({'success': False, 'message': 'Missing required fields'})
        
        # Check if user already exists
        if User.objects.filter(user_id=user_id).exists():
            return JsonResponse({'success': False, 'message': f'Teacher ID {user_id} already registered'})
        
        # Decode and save image
        try:
            image_bytes = base64.b64decode(image_data.split(',')[1])
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return JsonResponse({'success': False, 'message': 'Invalid image data'})
            
            # Save image
            os.makedirs('data/images', exist_ok=True)
            image_path = f'data/images/{user_id}.jpg'
            cv2.imwrite(image_path, frame)
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Image processing error: {str(e)}'})
        
        # Register face
        success, message = face_system.register_face(user_id, frame=frame)
        
        if not success:
            # Clean up image if face registration failed
            if os.path.exists(image_path):
                os.remove(image_path)
            return JsonResponse({'success': False, 'message': message})
        
        # Save to database
        try:
            user = User.objects.create(
                user_id=user_id,
                name=name,
                email=email,
                phone=phone,
                password=password
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully registered Teacher {name}!'
            })
            
        except IntegrityError:
            # Clean up if database save fails
            face_system.delete_user(user_id)
            if os.path.exists(image_path):
                os.remove(image_path)
            return JsonResponse({'success': False, 'message': 'Teacher already exists'})
            
    except Exception as e:
        import traceback
        print(f"Error in register_user: {traceback.format_exc()}")
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'})

def mark_attendance_page(request):
    """Kiosk Mode: Attendance marking page (Public access)"""
    total_registered = User.objects.count()
    today = date.today()
    marked_today = Attendance.objects.filter(date=today).count()
    
    context = {
        'total_registered': total_registered,
        'marked_today': marked_today,
    }
    return render(request, 'attendance/mark_attendance.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def process_attendance(request):
    """Process attendance from webcam frame (Public access)"""
    try:
        data = json.loads(request.body)
        image_data = data.get('image')
        
        if not image_data:
            return JsonResponse({'success': False, 'message': 'No image data provided'})
        
        # Decode base64 image
        try:
            image_bytes = base64.b64decode(image_data.split(',')[1])
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return JsonResponse({'success': False, 'message': 'Failed to decode image'})
            
        except Exception as img_error:
            return JsonResponse({'success': False, 'message': f'Image decode error: {str(img_error)}'})
        
        # Recognize faces
        try:
            recognized_faces = face_system.recognize_faces(frame)
        except Exception as rec_error:
            return JsonResponse({'success': False, 'message': f'Recognition error: {str(rec_error)}'})
        
        results = []
        today = date.today()
        
        for face_info in recognized_faces:
            name = face_info["name"]
            confidence = face_info["confidence"]
            location = face_info["location"]
            
            # Convert numpy int32 to Python int for JSON serialization
            location_tuple = tuple(int(x) for x in location)
            
            if name != "Unknown":
                try:
                    user = User.objects.get(user_id=name)
                    
                    # Try to mark attendance
                    attendance, created = Attendance.objects.get_or_create(
                        user=user,
                        date=today,
                        defaults={
                            'time': timezone.now().time(),
                            'timestamp': timezone.now()
                        }
                    )
                    
                    results.append({
                        'user_id': name,
                        'name': user.name,
                        'confidence': round(confidence * 100, 1),
                        'attendance_marked': created,
                        'location': location_tuple
                    })
                    
                except User.DoesNotExist:
                    print(f"User {name} not found in database")
            else:
                # Also return unknown faces for debugging
                results.append({
                    'user_id': 'unknown',
                    'name': 'Unknown',
                    'confidence': round(confidence * 100, 1),
                    'attendance_marked': False,
                    'location': location_tuple
                })
        
        return JsonResponse({'success': True, 'faces': results})
        
    except Exception as e:
        import traceback
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'})

@login_required
def user_detail(request, user_id):
    """View individual teacher details and history"""
    teacher = get_object_or_404(User, user_id=user_id)
    attendance_history = Attendance.objects.filter(user=teacher).order_by('-date')
    
    attendance_data = []
    for record in attendance_history:
        attendance_data.append({
            'date': record.date.strftime("%Y-%m-%d"),
            'time': record.time.strftime("%H:%M:%S"),
            'timestamp': record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    context = {
        'user_id': user_id,
        'teacher': {
            'name': teacher.name,
            'email': teacher.email or '',
            'phone': teacher.phone or '',
            'registered_at': teacher.registered_at.strftime("%Y-%m-%d %H:%M:%S")
        },
        'attendance_history': attendance_data,
        'total_days': len(attendance_data),
        'image_path': f'/media/images/{user_id}.jpg' if os.path.exists(f'data/images/{user_id}.jpg') else None
    }
    return render(request, 'attendance/user_detail.html', context)

@login_required
def statistics(request):
    """College Stats"""
    total_teachers = User.objects.count()
    today = date.today()
    present_today = Attendance.objects.filter(date=today).count()
    absent_today = total_teachers - present_today
    
    # Get attendance for last 7 days
    attendance_trend = []
    for i in range(6, -1, -1):
        check_date = today - timedelta(days=i)
        count = Attendance.objects.filter(date=check_date).count()
        attendance_trend.append({
            'date': check_date.strftime("%Y-%m-%d"),
            'count': count
        })
    
    context = {
        'total_teachers': total_teachers,
        'present_today': present_today,
        'absent_today': absent_today,
        'attendance_trend': attendance_trend,
        'today_date': today.strftime("%Y-%m-%d")
    }
    return render(request, 'attendance/statistics.html', context)

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
@login_required
def delete_user(request, user_id):
    """Delete a teacher"""
    try:
        # Get user
        user = get_object_or_404(User, user_id=user_id)
        user_name = user.name
        
        # Delete from face recognition system
        face_deleted = face_system.delete_user(user_id)
        
        # Delete user image if exists
        image_path = f'data/images/{user_id}.jpg'
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(f"Error deleting image: {e}")
        
        # Delete user (this will CASCADE delete all attendance records)
        user.delete()
        
        print(f"Teacher {user_id} ({user_name}) and all attendance records deleted successfully")
        return JsonResponse({
            'success': True,
            'message': f'Teacher {user_name} and all data deleted successfully'
        })
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error deleting teacher: {error_details}")
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'})

@login_required
def manage_timetable(request, user_id):
    """Admin view to manage teacher's timetable"""
    teacher = get_object_or_404(User, user_id=user_id)
    
    if request.method == 'POST':
        day = request.POST.get('day')
        subject = request.POST.get('subject')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        Timetable.objects.create(
            teacher=teacher,
            day_of_week=int(day),
            subject=subject,
            start_time=start_time,
            end_time=end_time
        )
        return redirect('manage_timetable', user_id=user_id)
        
    timetable = Timetable.objects.filter(teacher=teacher).order_by('day_of_week', 'start_time')
    return render(request, 'attendance/manage_timetable.html', {
        'teacher': teacher, 
        'timetable': timetable
    })

@login_required
def delete_timetable_slot(request, slot_id):
    """Delete a timetable slot"""
    if request.method == 'POST':
        slot = get_object_or_404(Timetable, id=slot_id)
        user_id = slot.teacher.user_id
        slot.delete()
        return redirect('manage_timetable', user_id=user_id)
    return redirect('index')

# Teacher Portal Views

def teacher_login(request):
    """Teacher Login Page"""
    if request.method == 'POST':
        # Check if it's a JSON request (Face Login)
        if request.content_type and request.content_type.startswith('application/json'):
            try:
                data = json.loads(request.body)
                image_data = data.get('image')
                
                if not image_data:
                    return JsonResponse({'success': False, 'message': 'No image provided'})
                
                # Decode image
                try:
                    image_bytes = base64.b64decode(image_data.split(',')[1])
                    nparr = np.frombuffer(image_bytes, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': 'Image decode failed'})

                # Recognize face
                recognized_faces = face_system.recognize_faces(frame)
                
                # Debug logging
                print(f"DEBUG: Login Attempt - Found {len(recognized_faces)} faces")
                for f in recognized_faces:
                    print(f"DEBUG: Face detected: {f['name']} with confidence {f['confidence']}")

                if not recognized_faces:
                    return JsonResponse({'success': False, 'message': 'No face detected'})
                
                # Check for match (highest confidence)
                best_match = None
                max_conf = 0
                
                for face in recognized_faces:
                    # Only accept if it's NOT Unknown
                    if face['name'] != "Unknown" and face['confidence'] > max_conf:
                        max_conf = face['confidence']
                        best_match = face['name']
                
                if best_match:
                    try:
                        teacher = User.objects.get(user_id=best_match)
                        request.session['teacher_id'] = teacher.user_id
                        from django.urls import reverse
                        print(f"DEBUG: Login Successful for {best_match}")
                        return JsonResponse({'success': True, 'redirect_url': reverse('teacher_dashboard')})
                    except User.DoesNotExist:
                        print(f"DEBUG: User {best_match} not found in DB")
                        return JsonResponse({'success': False, 'message': 'Face recognized but user not found'})
                else:
                    print("DEBUG: All faces were Unknown or below threshold")
                    return JsonResponse({'success': False, 'message': 'Face not recognized. Please try again or use password.'})
                    
            except Exception as e:
                import traceback
                print(f"DEBUG: Login Error: {traceback.format_exc()}")
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
                
        # Standard Password Login
        else:
            user_id = request.POST.get('user_id')
            password = request.POST.get('password')
            try:
                teacher = User.objects.get(user_id=user_id)
                if teacher.password == password:  # Note: Use hashed passwords in production
                    request.session['teacher_id'] = teacher.user_id
                    return redirect('teacher_dashboard')
                else:
                    return render(request, 'attendance/teacher_login.html', {'error': 'Invalid credentials'})
            except User.DoesNotExist:
                return render(request, 'attendance/teacher_login.html', {'error': 'Teacher ID not found'})
            
    return render(request, 'attendance/teacher_login.html')

def teacher_logout(request):
    """Logout Teacher"""
    if 'teacher_id' in request.session:
        del request.session['teacher_id']
    return redirect('teacher_login')

def teacher_dashboard(request):
    """Teacher Dashboard with Timetable"""
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')
    
    teacher = get_object_or_404(User, user_id=teacher_id)
    today = date.today()
    day_index = today.weekday()  # 0 = Monday
    
    # Get today's timetable
    timetable = Timetable.objects.filter(teacher=teacher, day_of_week=day_index).order_by('start_time')
    
    timetable_data = []
    current_time = datetime.now().time()
    
    for slot in timetable:
        # Check if attendance marked
        is_marked = LectureAttendance.objects.filter(
            teacher=teacher, 
            timetable=slot, 
            date=today
        ).exists()
        
        # Determine status
        status = 'Upcoming'
        if is_marked:
            status = 'Present'
        elif current_time > slot.end_time:
            status = 'Missed'
        elif current_time >= slot.start_time:
            status = 'Active'
            
        timetable_data.append({
            'id': slot.id,
            'subject': slot.subject,
            'start_time': slot.start_time,
            'end_time': slot.end_time,
            'is_marked': is_marked,
            'status': status
        })
        
    context = {
        'teacher': teacher,
        'timetable': timetable_data,
        'today': today,
        'day_name': today.strftime('%A')
    }
    return render(request, 'attendance/teacher_dashboard.html', context)

def mark_lecture_attendance(request, timetable_id):
    """Mark attendance for a specific lecture slot"""
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        return redirect('teacher_login')
        
    teacher = get_object_or_404(User, user_id=teacher_id)
    timetable = get_object_or_404(Timetable, id=timetable_id)
    
    # Security check: Ensure this timetable belongs to this teacher
    if timetable.teacher != teacher:
        return JsonResponse({'success': False, 'message': 'Unauthorized'})
        
    # Mark attendance
    LectureAttendance.objects.get_or_create(
        teacher=teacher,
        timetable=timetable,
        date=date.today(),
        defaults={'status': 'Present'}
    )
    
    return redirect('teacher_dashboard')
