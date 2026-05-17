import pandas as pd
import sqlite3
import time
import random
import os
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================
EXCEL_FILE = "leads.xlsx"
DB_FILE = "survey_database.db"
CALL_DELAY_SECONDS = 2  # Simulate time between calls
SIMULATION_SUCCESS_RATE = 0.8  # 80% chance they press 1

# ==========================================
# 1. DATABASE SETUP
# ==========================================
def init_database():
    """Creates the SQLite database and table if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            status TEXT DEFAULT 'pending',
            call_time TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {DB_FILE}")

# ==========================================
# 2. DATA LOADING (EXCEL -> DB)
# ==========================================
def load_leads_from_excel():
    """Reads Excel file and loads pending leads into the database."""
    if not os.path.exists(EXCEL_FILE):
        print(f"⚠️ {EXCEL_FILE} not found. Creating dummy data...")
        create_dummy_excel()
    
    df = pd.read_excel(EXCEL_FILE)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Clear previous run data for fresh demo
    cursor.execute("DELETE FROM participants")
    
    count = 0
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO participants (name, phone, status)
            VALUES (?, ?, 'pending')
        ''', (row['Name'], row['Phone']))
        count += 1
    
    conn.commit()
    conn.close()
    print(f"✅ Loaded {count} leads from Excel into Database.")

def create_dummy_excel():
    """Generates a sample Excel file for testing."""
    data = {
        'Name': ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Brown', 'Charlie Lee'],
        'Phone': ['+15550101', '+15550102', '+15550103', '+15550104', '+15550105']
    }
    df = pd.DataFrame(data)
    df.to_excel(EXCEL_FILE, index=False)
    print(f"📄 Created dummy file: {EXCEL_FILE}")

# ==========================================
# 3. MOCK TELEPHONY ENGINE
# ==========================================
def mock_make_call(phone_number):
    """
    SIMULATES a phone call. 
    In production, this is where you would use Twilio/Vonage API.
    """
    print(f"   📞 Dialing {phone_number}...")
    time.sleep(1) # Simulate connection time
    
    # Simulate connection success (95% chance call connects)
    if random.random() > 0.95:
        print("   ❌ Call Failed (No Answer/Busy)")
        return "no_answer"
    
    print("   🟢 Call Connected. Playing IVR Prompt...")
    time.sleep(1)
    print("   🗣️  Prompt: 'Press 1 to confirm survey participation.'")
    time.sleep(1)
    
    # Simulate User Input
    # In real life, this comes from the webhook callback
    if random.random() < SIMULATION_SUCCESS_RATE:
        print("   👆 User pressed 1")
        return "confirmed"
    else:
        print("   🚫 User did not press 1 or hung up")
        return "declined"

# ==========================================
# 4. MAIN AUTOMATION LOOP
# ==========================================
def run_automation():
    """Main loop that processes the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Fetch all pending participants
    cursor.execute("SELECT id, name, phone FROM participants WHERE status = 'pending'")
    leads = cursor.fetchall()
    
    if not leads:
        print("⚠️ No pending leads found.")
        return

    print(f"\n🚀 Starting Automation for {len(leads)} participants...\n")
    
    for lead_id, name, phone in leads:
        print(f"----------------------------------")
        print(f"👤 Contact: {name} ({phone})")
        
        # 1. Make the Call (Mock)
        result = mock_make_call(phone)
        
        # 2. Update Database based on result
        status = "completed"
        response = result
        call_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            UPDATE participants 
            SET status = ?, response = ?, call_time = ?
            WHERE id = ?
        ''', (status, response, call_time, lead_id))
        conn.commit()
        
        print(f"   💾 Database Updated: {status} - {response}")
        time.sleep(CALL_DELAY_SECONDS) # Be polite, don't rush
        
    conn.close()
    print("\n✅ Automation Cycle Complete.")

# ==========================================
# 5. REPORTING
# ==========================================
def show_results():
    """Prints a summary of the database status."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM participants", conn)
    conn.close()
    
    print("\n📊 FINAL RESULTS TABLE:")
    print(df.to_string(index=False))
    
    # Summary Stats
    total = len(df)
    confirmed = len(df[df['response'] == 'confirmed'])
    print(f"\n📈 Summary: {confirmed}/{total} Confirmed ({(confirmed/total)*100:.1f}%)")

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    init_database()
    load_leads_from_excel()
    run_automation()
    show_results()