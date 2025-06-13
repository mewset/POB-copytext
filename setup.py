"""
Setup script för POB-copytext
Kör detta en gång för att installera alla dependencies
"""

import subprocess
import sys
import os

def install_requirements():
    """Installera nödvändiga paket"""
    requirements = ['pyperclip']
    
    for package in requirements:
        try:
            print(f"Installerar {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installerat")
        except Exception as e:
            print(f"✗ Kunde inte installera {package}: {e}")
            return False
    
    return True

def create_launcher():
    """Skapa en launcher-fil"""
    launcher_content = f"""@echo off
cd /d "{os.path.abspath(os.path.dirname(__file__))}"
python app.py
pause
"""
    
    try:
        with open("Starta.bat", "w") as f:
            f.write(launcher_content)
        print("✓ Starta.bat skapad")
        return True
    except Exception as e:
        print(f"✗ Kunde inte skapa launcher: {e}")
        return False

def main():
    print("=== POB-Copytext ===")
    print("-- Skapat av MAAND19 --")
    print("Detta skript kommer att:")
    print("1. Installera nödvändiga Python-paket")
    print("2. Skapa en genväg för att starta programmet")
    print()
    
    input("Tryck Enter för att fortsätta...")
    
    # Installera requirements
    if not install_requirements():
        print("\nInstallation misslyckades!")
        input("Tryck Enter för att avsluta...")
        return
    
    # Skapa launcher
    if not create_launcher():
        print("\nKunde inte skapa launcher!")
        input("Tryck Enter för att avsluta...")
        return
    
    print("\n=== Setup komplett! ===")
    print("Du kan nu starta programmet genom att:")
    print("1. Dubbelklicka på 'starta.bat'")
    print("2. Eller köra 'app.py' direkt")
    print()
    input("Tryck Enter för att avsluta...")

if __name__ == "__main__":
    main()
