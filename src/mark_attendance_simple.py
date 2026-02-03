import cv2
import time
from datetime import datetime
from simple_face_recognition import SimpleFaceRecognitionSystem
from database import Database

def mark_attendance():
    """Real-time face recognition and attendance marking"""
    
    print("\n" + "="*60)
    print("       FACE ATTENDANCE SYSTEM - MARK ATTENDANCE")
    print("="*60 + "\n")
    
    # Initialize systems
    face_system = SimpleFaceRecognitionSystem()
    db = Database()
    
    # Check if any users are registered
    registered_users = face_system.get_registered_users()
    if not registered_users:
        print("❌ No users registered yet!")
        print("Please register users first using register_user_simple.py")
        return
    
    print(f"✅ {len(registered_users)} registered user(s) found")
    print("\nRegistered users:", ", ".join(registered_users))
    
    print("\n" + "-"*60)
    print("Starting attendance system...")
    print("Instructions:")
    print("  • Multiple faces can be detected simultaneously")
    print("  • Attendance is marked automatically when face is recognized")
    print("  • Each person can mark attendance once per day")
    print("  • Press 'q' to quit")
    print("-"*60 + "\n")
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot access webcam!")
        return
    
    # Track marked attendance for this session
    marked_today = set()
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load already marked attendance for today
    today_attendance = db.get_attendance_by_date(today)
    for record in today_attendance:
        marked_today.add(record["user_id"])
    
    print(f"📅 Date: {today}")
    if marked_today:
        print(f"✅ Already marked today: {', '.join(marked_today)}")
    print("\n🎥 Camera started. Detecting faces...\n")
    
    frame_count = 0
    process_every_n_frames = 2  # Process every 2nd frame for better performance
    recognized_faces = []
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            break
        
        frame_count += 1
        
        # Process face recognition every N frames
        if frame_count % process_every_n_frames == 0:
            recognized_faces = face_system.recognize_faces(frame)
        
        # Draw boxes and labels for all detected faces
        for face_info in recognized_faces:
            name = face_info["name"]
            confidence = face_info["confidence"]
            top, right, bottom, left = face_info["location"]
            
            # Choose color based on recognition
            if name == "Unknown":
                color = (0, 0, 255)  # Red for unknown
                label = "Unknown"
            else:
                color = (0, 255, 0)  # Green for recognized
                label = f"{name} ({confidence*100:.1f}%)"
                
                # Mark attendance if not already marked
                if name not in marked_today:
                    user_info = db.get_user(name)
                    if user_info:
                        success = db.mark_attendance(name, user_info["name"])
                        if success:
                            marked_today.add(name)
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            print(f"✅ [{timestamp}] Attendance marked for: {user_info['name']} (ID: {name})")
            
            # Draw rectangle around face
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            
            # Draw label background
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            # Draw label text
            cv2.putText(frame, label, (left + 6, bottom - 6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        # Display statistics
        stats_y = 30
        cv2.putText(frame, f"Date: {today}", (10, stats_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Registered: {len(registered_users)}", (10, stats_y + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Present: {len(marked_today)}", (10, stats_y + 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Detected: {len(recognized_faces)}", (10, stats_y + 90),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Display instructions
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Show frame
        cv2.imshow("Face Attendance System", frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Display summary
    print("\n" + "="*60)
    print("ATTENDANCE SUMMARY")
    print("="*60)
    print(f"Date: {today}")
    print(f"Total Registered: {len(registered_users)}")
    print(f"Present Today: {len(marked_today)}")
    
    if marked_today:
        print("\nAttendance marked for:")
        for user_id in marked_today:
            user_info = db.get_user(user_id)
            if user_info:
                print(f"  • {user_info['name']} (ID: {user_id})")
    
    absent = set(registered_users) - marked_today
    if absent:
        print("\nAbsent:")
        for user_id in absent:
            user_info = db.get_user(user_id)
            if user_info:
                print(f"  • {user_info['name']} (ID: {user_id})")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    mark_attendance()
