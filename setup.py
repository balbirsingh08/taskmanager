# setup.py
from database import SessionLocal, engine
import models
import schemas
import crud
import auth

# Create tables
models.Base.metadata.create_all(bind=engine)

def create_first_admin():
    db = SessionLocal()
    try:
        # Check if any users exist
        existing_users = db.query(models.User).all()
        print(f"Found {len(existing_users)} existing users")
        
        for user in existing_users:
            print(f"- {user.username} (role: {user.role})")
        
        # Create admin user if none exists
        if not existing_users:
            print("Creating first admin user...")
            admin_user = schemas.UserCreate(
                username="admin",
                password="admin123",
                role="admin"
            )
            created_user = crud.create_user(db, admin_user)
            print("✅ First admin user created successfully!")
            print(f"👤 Username: {created_user.username}")
            print(f"🔑 Password: admin123")
            print(f"🎯 Role: {created_user.role}")
        else:
            print("✅ Users already exist in database.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_first_admin()