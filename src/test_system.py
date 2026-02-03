#!/usr/bin/env python3
"""
Test script to verify the face attendance system is working correctly
"""

import cv2
import os
import sys

def test_webcam():
    """Test if webcam is accessible"""
    print("\n" + "="*60)
    print("TEST 1: Webcam Access")
    print("="*60)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ FAILED: Cannot access webcam")
        return False
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("❌ FAILED: Cannot capture frame")
        return False
    
    print("✅ PASSED: Webcam is working")
    print(f"   Frame size: {frame.shape[1]}x{frame.shape[0]}")
    return True

def test_face_detection():
    """Test if face detection is working"""
    print("\n" + "="*60)
    print("TEST 2: Face Detection")
    print("="*60)
    
    try:
        from simple_face_recognition import SimpleFaceRecognitionSystem
        
        face_system = SimpleFaceRecognitionSystem()
        print("✅ PASSED: Face recognition system initialized")
        
        # Test face cascade
        if face_system.face_cascade.empty():
            print("❌ FAILED: Face cascade not loaded")
            return False
        
        print("✅ PASSED: Face detection ready")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_database():
    """Test if database is working"""
    print("\n" + "="*60)
    print("TEST 3: Database System")
    print("="*60)
    
    try:
        from database import Database
        
        db = Database()
        print("✅ PASSED: Database initialized")
        
        # Check if data directory exists
        if not os.path.exists("data"):
            print("❌ FAILED: Data directory not found")
            return False
        
        print("✅ PASSED: Data directory exists")
        
        # Test database operations
        users = db.get_all_users()
        print(f"✅ PASSED: Database accessible ({len(users)} users registered)")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_opencv_contrib():
    """Test if opencv-contrib is installed with face module"""
    print("\n" + "="*60)
    print("TEST 4: OpenCV Face Module")
    print("="*60)
    
    try:
        import cv2
        
        # Try to create LBPH recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        print("✅ PASSED: OpenCV face module available")
        return True
        
    except AttributeError:
        print("❌ FAILED: OpenCV face module not found")
        print("   Run: pip install opencv-contrib-python==4.8.1.78")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 FACE ATTENDANCE SYSTEM - SYSTEM TEST")
    print("="*60)
    
    tests = [
        test_webcam,
        test_opencv_contrib,
        test_face_detection,
        test_database
    ]
    
    results = []
    
    for test in tests:
        results.append(test())
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nYour system is ready to use. Run:")
        print("   python main.py")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("\nPlease fix the issues above before using the system.")
    
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    # Change to src directory if not already there
    if os.path.basename(os.getcwd()) != "src":
        if os.path.exists("src"):
            os.chdir("src")
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
