# 🚀 LIVE TEST GUIDE: Real-Time Volunteer Notifications

## Quick Start (2 minutes)

### Step 1: Start the Flask App
```bash
cd /Users/ramavathvarun/Downloads/disaster_management
python3 app.py
```
You should see:
```
Running on http://127.0.0.1:5001
WARNING in werkzeug: [...]
```

### Step 2: Start ngrok (in another terminal)
```bash
cd /Users/ramavathvarun/Downloads/disaster_management
./ngrok http 5001
```
You should see:
```
Session Status                online
Forwarding                    https://adele-unfocused-scientifically.ngrok-free.dev -> http://localhost:5001
```

### Step 3: Open Two Browser Tabs
- **Tab 1 (Official User)**: `https://adele-unfocused-scientifically.ngrok-free.dev/volunteer_management`
- **Tab 2 (Volunteer User)**: Login as volunteer `maxx` or `demo`

## The Test Flow

### In Tab 1 (Official User):
1. Go to Volunteer Management page
2. Select a hazard from dropdown (e.g., "High Rain Alert")
3. See list of nearby volunteers
4. Click **"Assign Volunteer"** button next to a volunteer

### In Tab 2 (Volunteer User):
5. **Watch the bell icon** in navbar
   - Should show red badge with number **within 3 seconds**
   
6. **Watch for toast notification** (top-right corner)
   - Should slide in with message: "🔔 New Notification! You have a new assignment notification."
   
7. **Click on the notification badge** or go to `/notifications`
   - Should see the assignment with **"Accept"** and **"Decline"** buttons
   
8. **Click "Accept"** to accept the assignment
   - Status should change to green checkmark
   - Badge should decrease or disappear

## Expected Timeline

| Step | Action | Expected Delay |
|------|--------|-----------------|
| Click "Assign Volunteer" | Backend processes | <1 second |
| Notification created | Database write | <1 second |
| Volunteer's browser polls | API endpoint | 0-3 seconds (3-second interval) |
| Badge appears | DOM update | <100ms |
| Toast appears | Visual notification | <100ms |
| Volunteer sees notification | Notification page loads | Instant |

**Total latency: <3 seconds** ✅

## What to Verify

### ✅ Badge System
- [ ] Red badge appears on bell icon
- [ ] Badge shows correct count
- [ ] Badge updates when more assignments come in
- [ ] Badge disappears when notifications are viewed

### ✅ Toast System
- [ ] Toast slides in from right side
- [ ] Toast shows blue box with bell icon
- [ ] Toast has "View Notification" button
- [ ] Toast auto-dismisses after 5 seconds
- [ ] Toast doesn't appear more than once per 10 seconds

### ✅ Notification Page
- [ ] Shows assignment details
- [ ] Shows "Accept" button in blue
- [ ] Shows "Decline" button in red
- [ ] Clicking "Accept" changes status to ✅
- [ ] Clicking "Decline" changes status to ✗
- [ ] Assignment appears immediately after button click

### ✅ Real-Time Updates
- [ ] No page refresh needed to see notification
- [ ] Badge updates automatically every 3 seconds
- [ ] Multiple assignments stack properly
- [ ] Notifications persist across page refreshes

## Troubleshooting

### "No notification appeared"
1. Check browser console for errors: `F12 → Console tab`
2. Verify polling is running: Look for "Notification poll" messages
3. Check network tab: Look for requests to `/api/notifications/unread-count`
4. Verify volunteer is logged in (check `current_user` in browser console)

### "Toast not appearing but badge is"
1. Check if `showNotificationToast()` function exists in base.html
2. Look for JavaScript errors in console
3. Try refreshing page

### "App won't start"
```bash
# Check if port 5001 is in use
lsof -i :5001

# If in use, kill the process
kill -9 <PID>

# Or use a different port
python3 app.py --port 5002
```

## Advanced Testing

### Test Multiple Simultaneous Assignments
1. Click "Assign Volunteer" button multiple times in quick succession
2. Volunteer should see multiple toast notifications
3. Badge count should be 2, 3, etc.

### Test Assignment Recovery
1. Assign a volunteer
2. Volunteer navigates away from page
3. Navigates back
4. Should still see assignment notification

### Test Notification Cleanup
1. Accept an assignment
2. Notification should move to "read" section
3. Badge count should decrease

## Key Code Locations

- **Real-time polling**: `templates/base.html` line 1448 (every 3 seconds)
- **Toast function**: `templates/base.html` line 1398-1444 (shows notification)
- **Assign button**: `templates/volunteer_management.html` line 855-910
- **API endpoint**: `routes/coordination.py` (creates assignment)
- **Notification page**: `templates/notifications.html` (auto-refreshes)

## Success Criteria

✅ **You have successfully fixed the notification system when:**

1. Click "Assign Volunteer" in Tab 1
2. Within 3 seconds, Tab 2 shows:
   - Red badge with number on bell icon
   - Toast notification sliding in from right
   - Optional: Sound or browser notification
3. Click bell icon to go to notifications page
4. See assignment with "Accept" and "Decline" buttons
5. Click "Accept" and see status change immediately

## Database Commands (If Needed)

Check notifications were created:
```bash
python3 -c "
from app import app, db
from models import Notification
with app.app_context():
    count = Notification.query.count()
    print(f'Total notifications: {count}')
    recent = Notification.query.order_by(Notification.created_at.desc()).limit(5).all()
    for n in recent:
        print(f'- {n.user_id}: {n.message[:50]}...')
"
```

Check assignments were created:
```bash
python3 -c "
from app import app, db
from models import VolunteerAssignment
with app.app_context():
    count = VolunteerAssignment.query.count()
    print(f'Total assignments: {count}')
    recent = VolunteerAssignment.query.order_by(VolunteerAssignment.created_at.desc()).limit(5).all()
    for a in recent:
        print(f'- Volunteer {a.volunteer_id}: {a.status}')
"
```

---

**System Status**: ✅ Ready for Testing
**Last Updated**: Just now
**Version**: Real-Time Polling v3 (3-second intervals)
