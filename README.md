```bash
(venv) pulkit3010:~/Documents/Projects$ python auto_survery.py 
✅ Database initialized: survey_database.db
⚠️ leads.xlsx not found. Creating dummy data...
📄 Created dummy file: leads.xlsx
✅ Loaded 5 leads from Excel into Database.

🚀 Starting Automation for 5 participants...

----------------------------------
👤 Contact: John Doe (15550101)
   📞 Dialing 15550101...
   🟢 Call Connected. Playing IVR Prompt...
   🗣️  Prompt: 'Press 1 to confirm survey participation.'
   👆 User pressed 1
   💾 Database Updated: completed - confirmed
----------------------------------
👤 Contact: Jane Smith (15550102)
   📞 Dialing 15550102...
   🟢 Call Connected. Playing IVR Prompt...
   🗣️  Prompt: 'Press 1 to confirm survey participation.'
   👆 User pressed 1
   💾 Database Updated: completed - confirmed
----------------------------------
👤 Contact: Alice Johnson (15550103)
   📞 Dialing 15550103...
   🟢 Call Connected. Playing IVR Prompt...
   🗣️  Prompt: 'Press 1 to confirm survey participation.'
   🚫 User did not press 1 or hung up
   💾 Database Updated: completed - declined
----------------------------------
👤 Contact: Bob Brown (15550104)
   📞 Dialing 15550104...
   🟢 Call Connected. Playing IVR Prompt...
   🗣️  Prompt: 'Press 1 to confirm survey participation.'
   👆 User pressed 1
   💾 Database Updated: completed - confirmed
----------------------------------
👤 Contact: Charlie Lee (15550105)
   📞 Dialing 15550105...
   🟢 Call Connected. Playing IVR Prompt...
   🗣️  Prompt: 'Press 1 to confirm survey participation.'
   🚫 User did not press 1 or hung up
   💾 Database Updated: completed - declined

✅ Automation Cycle Complete.

📊 FINAL RESULTS TABLE:
 id          name    phone    status           call_time  response
  1      John Doe 15550101 completed 2026-05-17 18:57:24 confirmed
  2    Jane Smith 15550102 completed 2026-05-17 18:57:29 confirmed
  3 Alice Johnson 15550103 completed 2026-05-17 18:57:34  declined
  4     Bob Brown 15550104 completed 2026-05-17 18:57:39 confirmed
  5   Charlie Lee 15550105 completed 2026-05-17 18:57:44  declined

📈 Summary: 3/5 Confirmed (60.0%)
```