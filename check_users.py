  # check_users.py
from database import SessionLocal
import models

def check_existing_users():
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        print("Existing users in database:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}, Password Hash: {user.password}")
        
        if not users:
            print("No users found in database!")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_existing_users()