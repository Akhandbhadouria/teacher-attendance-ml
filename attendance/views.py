from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
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
from .models import User, Attendance

# Initialize face recognition system
face_system = SimpleFaceRecognitionSystem()

def index(request):
    """Home page"""
    total_users = User.objects.count()
    today = date.today()
    present_today = Attendance.objects.filter(date=today).count()
    absent_today = total_users - present_today
    
    context = {
        'total_users': total_users,
        'present_today': present_today,
        'absent_today': absent_today,
    }
    return render(request, 'attendance/index.html', context)

def users_list(request):
    """List all registered users"""
    users = User.objects.all()
    
    users_data = []
    for user in users:
        users_data.append({
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email or 'N/A',
            'phone': user.phone or 'N/A',
            'registered_at': user.registered_at.strftime("%Y-%m-%d %H:%M:%S"),
            'image_path': f'/media/images/{user.user_id}.jpg' if os.path.exists(f'data/images/{user.user_id}.jpg') else None
        })
    
    context = {'users': users_data}
    return render(request, 'attendance/users.html', context)

def attendance_records(request):
    """View attendance records"""
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

def register_page(request):
    """Registration page"""
    return render(request, 'attendance/register.html')

@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    """Register a new user"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        name = data.get('name')
        email = data.get('email', '')
        phone = data.get('phone', '')
        image_data = data.get('image')
        
        if not all([user_id, name, image_data]):
            return JsonResponse({'success': False, 'message': 'Missing required fields'})
        
        # Check if user already exists
        if User.objects.filter(user_id=user_id).exists():
            return JsonResponse({'success': False, 'message': f'User ID {user_id} already registered'})
        
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
                phone=phone
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Successfully registered {name}!'
            })
            
        except IntegrityError:
            # Clean up if database save fails
            face_system.delete_user(user_id)
            if os.path.exists(image_path):
                os.remove(image_path)
            return JsonResponse({'success': False, 'message': 'User already exists'})
            
    except Exception as e:
        import traceback
        print(f"Error in register_user: {traceback.format_exc()}")
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'})

def mark_attendance_page(request):
    """Attendance marking page"""
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
    """Process attendance from webcam frame"""
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
            
            print(f"Frame decoded successfully: {frame.shape}")
        except Exception as img_error:
            print(f"Image decode error: {img_error}")
            return JsonResponse({'success': False, 'message': f'Image decode error: {str(img_error)}'})
        
        # Recognize faces
        try:
            recognized_faces = face_system.recognize_faces(frame)
            print(f"Recognized {len(recognized_faces)} face(s)")
        except Exception as rec_error:
            print(f"Recognition error: {rec_error}")
            return JsonResponse({'success': False, 'message': f'Recognition error: {str(rec_error)}'})
        
        results = []
        today = date.today()
        
        for face_info in recognized_faces:
            name = face_info["name"]
            confidence = face_info["confidence"]
            location = face_info["location"]
            
            # Convert numpy int32 to Python int for JSON serialization
            location_tuple = tuple(int(x) for x in location)
            
            print(f"Detected face: {name}, confidence: {confidence:.2%}")
            
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
                    
                    print(f"Attendance marking for {name}: {'Success' if created else 'Already marked'}")
                    
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
        
        print(f"Returning {len(results)} results")
        return JsonResponse({'success': True, 'faces': results})
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in process_attendance: {error_details}")
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'})

def user_detail(request, user_id):
    """View individual user details and attendance history"""
    user = get_object_or_404(User, user_id=user_id)
    attendance_history = Attendance.objects.filter(user=user).order_by('-date')
    
    attendance_data = []
    for record in attendance_history:
        attendance_data.append({
            'date': record.date.strftime("%Y-%m-%d"),
            'time': record.time.strftime("%H:%M:%S"),
            'timestamp': record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    context = {
        'user_id': user_id,
        'user': {
            'name': user.name,
            'email': user.email or '',
            'phone': user.phone or '',
            'registered_at': user.registered_at.strftime("%Y-%m-%d %H:%M:%S")
        },
        'attendance_history': attendance_data,
        'total_days': len(attendance_data),
        'image_path': f'/media/images/{user_id}.jpg' if os.path.exists(f'data/images/{user_id}.jpg') else None
    }
    return render(request, 'attendance/user_detail.html', context)

def statistics(request):
    """View attendance statistics"""
    total_users = User.objects.count()
    today = date.today()
    present_today = Attendance.objects.filter(date=today).count()
    absent_today = total_users - present_today
    
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
        'total_users': total_users,
        'present_today': present_today,
        'absent_today': absent_today,
        'attendance_trend': attendance_trend,
        'today_date': today.strftime("%Y-%m-%d")
    }
    return render(request, 'attendance/statistics.html', context)

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def delete_user(request, user_id):
    """Delete a user from the system"""
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
        
        print(f"User {user_id} ({user_name}) and all attendance records deleted successfully")
        return JsonResponse({
            'success': True,
            'message': f'User {user_name} and all attendance records deleted successfully'
        })
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error deleting user: {error_details}")
        return JsonResponse({'success': False, 'message': f'Server error: {str(e)}'})
