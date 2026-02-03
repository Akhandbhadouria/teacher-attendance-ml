#!/usr/bin/env python
"""
Test script to debug face recognition and attendance marking
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database import Database
from simple_face_recognition import SimpleFaceRecognitionSystem
import cv2

def test_system():
    print("=" * 60)
    print("FACE ATTENDANCE SYSTEM - DEBUG TEST")
    print("=" * 60)
    
    # Initialize systems
    print("\n1. Initializing systems...")
    db = Database()
    face_system = SimpleFaceRecognitionSystem()
    
    # Check registered users
    print("\n2. Checking registered users...")
    users = db.get_all_users()
    print(f"   Total users in database: {len(users)}")
    for user_id, user_info in users.items():
        print(f"   - {user_id}: {user_info['name']}")
    
    # Check face recognition system
    print("\n3. Checking face recognition system...")
    registered_faces = face_system.get_registered_users()
    print(f"   Total faces registered: {len(registered_faces)}")
    for name in registered_faces:
        print(f"   - {name}")
    
    # Check if model is trained
    print("\n4. Checking trained model...")
    model_path = "data/models/face_recognizer.yml"
    if os.path.exists(model_path):
        print(f"   ✅ Model exists: {model_path}")
        file_size = os.path.getsize(model_path)
        print(f"   Model size: {file_size} bytes")
    else:
        print(f"   ❌ Model not found!")
    
    # Check encodings
    print("\n5. Checking face encodings...")
    names_file = "data/encodings/names.pkl"
    samples_file = "data/encodings/samples.pkl"
    
    if os.path.exists(names_file):
        print(f"   ✅ Names file exists")
    else:
        print(f"   ❌ Names file missing!")
    
    if os.path.exists(samples_file):
        print(f"   ✅ Samples file exists")
        file_size = os.path.getsize(samples_file)
        print(f"   Samples size: {file_size} bytes")
    else:
        print(f"   ❌ Samples file missing!")
    
    # Check attendance records
    print("\n6. Checking attendance records...")
    today = "2026-02-03"
    attendance = db.get_attendance_by_date(today)
    print(f"   Attendance for {today}: {len(attendance)} records")
    for record in attendance:
        print(f"   - {record['user_id']}: {record['name']} at {record['time']}")
    
    # Test camera
    print("\n7. Testing camera access...")
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("   ✅ Camera is accessible")
            ret, frame = cap.read()
            if ret:
                print(f"   ✅ Can capture frames: {frame.shape}")
                
                # Test face detection
                print("\n8. Testing face detection...")
                faces, gray = face_system.detect_faces(frame)
                print(f"   Detected {len(faces)} face(s) in current frame")
                
                if len(faces) > 0:
                    # Test recognition
                    print("\n9. Testing face recognition...")
                    recognized = face_system.recognize_faces(frame)
                    for face_info in recognized:
                        print(f"   - Name: {face_info['name']}")
                        print(f"     Confidence: {face_info['confidence']:.2%}")
                        print(f"     Location: {face_info['location']}")
                
            else:
                print("   ❌ Cannot capture frames")
            cap.release()
        else:
            print("   ❌ Cannot open camera")
    except Exception as e:
        print(f"   ❌ Camera error: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_system()
