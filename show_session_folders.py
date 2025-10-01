#!/usr/bin/env python3
"""
WhatsApp Session Folder Explorer
Shows you where session data is stored to avoid QR scanning
"""

import os
import datetime

def show_session_folders():
    """Display all WhatsApp session folders and their contents"""
    
    print("📁 WhatsApp Session Storage Locations")
    print("=" * 50)
    
    # Main session directory
    main_dir = r"C:\num\whatsapp_sessions"
    print(f"🗂️  Main Sessions Directory: {main_dir}")
    
    if not os.path.exists(main_dir):
        print("❌ No session directory found yet.")
        print("💡 Run 'python enhanced_whatsapp_checker.py' to create it")
        return
    
    print(f"📊 Directory exists: {os.path.exists(main_dir)}")
    print()
    
    # List all sessions
    sessions = []
    try:
        for item in os.listdir(main_dir):
            item_path = os.path.join(main_dir, item)
            if os.path.isdir(item_path):
                sessions.append(item)
        
        if not sessions:
            print("📭 No sessions found yet")
            print("💡 Create a session by running the checker")
            return
        
        print(f"🎯 Found {len(sessions)} session(s):")
        print()
        
        for i, session in enumerate(sessions, 1):
            session_path = os.path.join(main_dir, session)
            print(f"📂 {i}. Session: {session}")
            print(f"   📍 Path: {session_path}")
            
            # Get session size
            total_size = 0
            file_count = 0
            
            for root, dirs, files in os.walk(session_path):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        total_size += os.path.getsize(file_path)
                        file_count += 1
                    except:
                        pass
            
            size_mb = round(total_size / (1024 * 1024), 2)
            print(f"   💾 Size: {size_mb} MB ({file_count} files)")
            
            # Check for key WhatsApp files
            profile_path = os.path.join(session_path, "WhatsAppProfile")
            if os.path.exists(profile_path):
                key_files = ["Cookies", "Local Storage", "Session Storage", "Preferences"]
                found_files = []
                
                for key_file in key_files:
                    key_path = os.path.join(profile_path, key_file)
                    if os.path.exists(key_path):
                        found_files.append(key_file)
                
                if found_files:
                    print(f"   🔑 WhatsApp Data: {', '.join(found_files)}")
                    print(f"   ✅ Status: Ready to use (no QR scan needed)")
                else:
                    print(f"   ⚠️  Status: Empty session (QR scan required)")
            else:
                print(f"   ❌ Status: No profile data")
            
            # Get creation/modification time
            try:
                mod_time = os.path.getmtime(session_path)
                mod_date = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                print(f"   📅 Last Modified: {mod_date}")
            except:
                pass
            
            print()
    
    except Exception as e:
        print(f"❌ Error reading sessions: {e}")

def show_session_structure():
    """Show the internal structure of a session folder"""
    
    print("\n📋 Session Folder Structure")
    print("=" * 30)
    print("WhatsApp session data is stored in:")
    print()
    print("C:\\num\\whatsapp_sessions\\")
    print("├── session_name_1\\")
    print("│   └── WhatsAppProfile\\")
    print("│       ├── Cookies                  # 🍪 Login cookies")
    print("│       ├── Local Storage\\          # 💾 WhatsApp data")
    print("│       ├── Session Storage\\        # 🔄 Session info")
    print("│       ├── Preferences             # ⚙️  Browser settings")
    print("│       └── Cache\\                  # 📦 Cached files")
    print("├── session_name_2\\")
    print("└── session_name_3\\")
    print()
    print("🔑 Key Points:")
    print("   • Each session = one WhatsApp login")
    print("   • Cookies file contains login token")
    print("   • Local Storage has WhatsApp messages/contacts")
    print("   • Session persists until WhatsApp logs you out")
    print("   • Backup these folders to save login sessions")

def main():
    """Main function"""
    print("🔍 WhatsApp Session Folder Explorer")
    print("📊 See where your login data is stored")
    print()
    
    show_session_folders()
    show_session_structure()
    
    print("\n💡 Usage Tips:")
    print("   1. Run 'python enhanced_whatsapp_checker.py' first")
    print("   2. Scan QR code once to create session")
    print("   3. Session will be saved automatically")
    print("   4. Next time: no QR scan needed!")
    print()
    print("🗂️  To backup a session:")
    print("   Copy the entire session folder to a safe location")
    print()
    print("🔄 To restore a session:")
    print("   Copy the backup folder back to whatsapp_sessions\\")

if __name__ == "__main__":
    main()