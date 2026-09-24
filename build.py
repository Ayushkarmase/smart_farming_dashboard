import os
import shutil
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
PUBLIC_STATIC_DIR = os.path.join(PUBLIC_DIR, 'static')
REDIRECTS_FILE = os.path.join(PUBLIC_DIR, '_redirects')

def build():
    print("==================================================")
    print(" Starting Netlify Build: Smart Farming Dashboard ")
    print("==================================================")

    # 1. Ensure public directories exist
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    os.makedirs(PUBLIC_STATIC_DIR, exist_ok=True)

    # 2. Copy static assets to public/static
    if os.path.exists(STATIC_DIR):
        print(f"-> Copying static assets from {STATIC_DIR} to {PUBLIC_STATIC_DIR}...")
        shutil.copytree(STATIC_DIR, PUBLIC_STATIC_DIR, dirs_exist_ok=True)
        print("   Static assets synchronized successfully.")
    else:
        print("! Warning: static directory not found.")

    # 3. Create public/_redirects file
    redirects_content = (
        "/static/*  /static/:splat  200\n"
        "/*         /.netlify/functions/app  200!\n"
    )
    # newline='' + explicit \n ensures LF-only endings on all platforms
    with open(REDIRECTS_FILE, 'w', encoding='utf-8', newline='') as f:
        f.write(redirects_content)
    print("-> Generated public/_redirects rule set.")

    # 4. Initialize and seed SQLite database
    print("-> Verifying and seeding SQLite database baseline...")
    try:
        from database.db_init import init_db
        init_db()
        print("   SQLite baseline database ready.")
    except Exception as e:
        print(f"! Warning initializing database: {e}")

    print("==================================================")
    print(" Netlify Build completed successfully! ")
    print("==================================================")

if __name__ == '__main__':
    build()
