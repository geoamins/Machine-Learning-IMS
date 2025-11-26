"""
Quick script to verify your setup is ready for Streamlit Cloud deployment.
Run this before deploying to catch any issues early.
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and return status"""
    exists = os.path.exists(filepath)
    status = "[OK]" if exists else "[MISSING]"
    print(f"{status} {description}: {filepath}")
    return exists

def check_requirements():
    """Check if requirements.txt has necessary packages"""
    req_file = 'requirements.txt'
    if not os.path.exists(req_file):
        print(f"❌ requirements.txt not found!")
        return False
    
    required_packages = ['streamlit', 'pandas', 'scikit-learn']
    with open(req_file, 'r') as f:
        content = f.read().lower()
    
    missing = []
    for pkg in required_packages:
        if pkg not in content:
            missing.append(pkg)
    
    if missing:
        print(f"[MISSING] Missing packages in requirements.txt: {', '.join(missing)}")
        return False
    else:
        print(f"[OK] requirements.txt contains all necessary packages")
        return True

def main():
    # Set UTF-8 encoding for Windows compatibility
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("Checking Streamlit Cloud Readiness")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check main files
    print("Checking Required Files:")
    print("-" * 60)
    all_good &= check_file_exists('streamlit_app.py', 'Main Streamlit app')
    all_good &= check_file_exists('Book1.csv', 'Data file')
    all_good &= check_file_exists('requirements.txt', 'Dependencies file')
    
    print()
    print("Checking Dependencies:")
    print("-" * 60)
    all_good &= check_requirements()
    
    print()
    print("=" * 60)
    if all_good:
        print("All checks passed! You're ready for Streamlit Cloud!")
        print()
        print("Next steps:")
        print("1. Push to GitHub: git add . && git commit -m 'Ready' && git push")
        print("2. Go to https://share.streamlit.io/")
        print("3. Deploy with path: ML Week 7/Bayesian Classification/streamlit_app.py")
    else:
        print("Some checks failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("- Make sure all files are in the same directory")
        print("- Check that Book1.csv is committed to Git")
        print("- Verify requirements.txt has all packages")
    print("=" * 60)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())

