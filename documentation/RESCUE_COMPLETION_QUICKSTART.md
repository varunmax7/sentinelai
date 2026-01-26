# Quick Start: Testing Rescue Completion System

## Start the App

```bash
cd /Users/ramavathvarun/Downloads/disaster_management
source venv/bin/activate
flask run
```

The app will be available at `http://localhost:5000`

---

## 1. Test Rescue Completion Form

### Step 1: Login as a Volunteer
- Go to `http://localhost:5000/login`
- Login with a volunteer account (or register as volunteer first)

### Step 2: Accept an Assignment
- Go to `http://localhost:5000/notifications`
- Click "Accept" on an emergency assignment
- Note the assignment ID from the URL or the notification

### Step 3: Navigate to Rescue Complete Form
- Go to `http://localhost:5000/rescue-complete?assignment_id=1`
  (Replace 1 with your actual assignment ID)

### Expected Form Display:
- ✓ Hazard information card
- ✓ Location verification section with "Get Location" button
- ✓ Photo upload area (drag-drop or click)
- ✓ Rescue notes textarea
- ✓ Submit button (disabled until location verified)

### Step 4: Get Location
- Click "Get Location" button
- Browser will request Geolocation permission - Allow it
- Form should show:
  - Your current coordinates
  - Distance to hazard
  - Green status if within 500m
  - Red status if too far

### Step 5: Upload Photo
- Drag & drop a photo (JPEG/PNG/GIF/WebP, max 5MB)
- Or click photo area to select file

### Step 6: Add Notes (Optional)
- Type rescue notes in the textarea

### Step 7: Submit (If Within 500m)
- Click "Mark Rescue Complete" button
- Should show success message with points earned

---

## 2. Test Leaderboard

### Public Leaderboard Page
- Navigate to `http://localhost:5000/leaderboard`
- Should display all volunteers sorted by points

### View Your Rank
- Go to `http://localhost:5000/api/leaderboard/user/YOUR_USER_ID`
- Returns your rank and stats in JSON

---

## 3. API Testing

### Test with curl

#### Complete a Rescue
```bash
curl -X POST http://localhost:5000/api/coordination/assignment/1/complete \
  -H "Content-Type: application/json" \
  -d '{
    "photo_url": "https://example.com/photo.jpg",
    "notes": "Rescue completed successfully",
    "latitude": 40.7128,
    "longitude": -74.0060
  }'
```

#### Get Leaderboard
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/leaderboard?page=1&per_page=50
```

#### Get User Rank
```bash
curl http://localhost:5000/api/leaderboard/user/5
```

---

## 4. Expected Points Distribution

| Experience | Time | Points |
|---|---|---|
| Beginner | Same day (< 12h) | 100 + 20 = **120** |
| Beginner | Next day (24h+) | **100** |
| Intermediate | Same day (< 4h) | 150 + 30 = **180** |
| Intermediate | Next day (24h+) | **150** |
| Expert | Immediate (< 1h) | 200 + 30 = **230** |
| Expert | Next day (24h+) | **200** |

---

## 5. Troubleshooting

### Issue: Form not loading
- Check volunteer has accepted assignment
- Verify assignment ID is correct
- Check browser console for errors (F12)

### Issue: "You are too far away"
- Form requires being within 500 meters
- Test locally or move to a location near hazard
- For testing, you can temporarily modify distance check in `app.py` line 3346

### Issue: Photo upload fails
- Check file size (must be < 5MB)
- Verify file format (JPEG/PNG/GIF/WebP)
- Check browser console for errors

### Issue: "Location access denied"
- Browser Geolocation permission rejected
- Allow location access in browser settings
- On HTTPS-only browsers (production), use HTTPS

### Issue: Points not awarded
- Verify distance is within 500m
- Check assignment status is "accepted"
- Verify photo_url is provided

---

## 6. Database Verification

### Check if columns exist
```bash
python -c "
import sqlite3
conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(volunteers);')
for col in cursor.fetchall():
    print(col[1])
conn.close()
"
```

Should include: `points`, `total_rescues`

### Check volunteer records
```bash
python -c "
from app import app, db
from models import Volunteer
with app.app_context():
    v = Volunteer.query.first()
    if v:
        print(f'Volunteer: {v.user.username}, Points: {v.points}, Rescues: {v.total_rescues}')
    else:
        print('No volunteers found')
"
```

---

## 7. Quick Test Workflow

**Total time: ~5 minutes**

1. **Login** - 30 seconds
2. **Accept assignment** - 30 seconds
3. **Navigate to form** - 10 seconds
4. **Get location** - 30 seconds
5. **Upload photo** - 1 minute
6. **Submit form** - 10 seconds
7. **View success** - 30 seconds
8. **Check leaderboard** - 1 minute

---

## 8. Key URLs

| Purpose | URL |
|---|---|
| Rescue Form | `/rescue-complete?assignment_id=1` |
| Leaderboard | `/leaderboard` |
| API Leaderboard | `/api/leaderboard?page=1&per_page=50` |
| User Rank | `/api/leaderboard/user/5` |
| Notifications | `/notifications` |
| Complete Rescue (API) | `POST /api/coordination/assignment/1/complete` |

---

## 9. Sample Test Data

### If you have test volunteers/emergencies:
- Volunteer 1: John (Beginner) - 0 points, 0 rescues
- Volunteer 2: Jane (Expert) - 0 points, 0 rescues
- Emergency 1: Building collapse - Location: (40.7128, -74.0060)

After completion:
- If Jane completes in 2 hours: 200 + 27 = **227 points**
- Jane moves to Rank 1 on leaderboard
- Notification sent to person who assigned the task

---

## 10. Success Indicators

✅ System is working if you see:

1. **Form page loads** without errors
2. **Location button works** and shows your coordinates
3. **Distance calculates** and displays correctly
4. **Photo upload** accepts files
5. **Submit button enabled** when within 500m
6. **Success message** shows points earned
7. **Leaderboard updated** with your new points
8. **Rank changes** on `/api/leaderboard/user/{id}`

---

**Ready to test! 🚀**
