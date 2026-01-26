# 🧪 Testing the Volunteer Assignment & Notification System

## Quick Test Guide

### Prerequisites
1. Flask app running: `python3 app.py`
2. ngrok tunnel active: `./ngrok http 5001`
3. Access via ngrok URL (shown in terminal)

---

## Test Scenario: Assigning a Volunteer to a Hazard

### Step 1: Official User Logs In
- Navigate to the app
- Login as an **Official** or **Analyst** user
- Example: Username `varunmax7`, role: Official

### Step 2: Go to Volunteer Management
- Click: **Coordination Dashboard** or **Volunteer Management**
- Should see: "Assign Volunteers to Hazard" section

### Step 3: Select a Hazard
- Click dropdown: "Select Hazard/Emergency"
- Choose any hazard/emergency (e.g., "Tsunami by @maxx")
- The page should automatically load nearby volunteers

### Step 4: Assign a Volunteer
- Click the blue "Assign Volunteer" button on any volunteer card
- You should see:
  - ✅ Button shows loading: "Assigning..." with spinner
  - ✅ Success modal appears: "Successfully Assigned!"
  - ✅ List refreshes automatically

### Step 5: Volunteer User Receives Notification
**In a separate browser/tab**, login as the **Volunteer** user:

#### Option A: Already on the App
- Look at the **bell icon** (top right) in the navbar
- ✅ Should see a red badge with a number
- ✅ Toast notification appears: "New Notification! You have a new assignment."

#### Option B: Check Notifications Page
- Click the **bell icon** or go to **Notifications** page
- ✅ Should see new entry: "You have been assigned to help with hazard: [Hazard Name]"
- ✅ Can click "Accept" or "Decline"

---

## Expected Behavior Timeline

| Time | Event | Expected Result |
|------|-------|-----------------|
| T+0s | Official clicks "Assign Volunteer" | Button shows "Assigning..." spinner |
| T+1s | Assignment created in database | Backend creates Notification record |
| T+5s | Polling detects new notification | Notification badge appears on bell |
| T+5.5s | Toast notification shown | "New Notification!" appears top-right |
| T+6s | Volunteer visits Notifications | New assignment visible in list |

---

## Verification Checklist

### ✅ Visual Indicators
- [ ] Notification badge appears on bell icon
- [ ] Badge shows correct unread count
- [ ] Toast notification pops up
- [ ] Notifications page auto-refreshes
- [ ] Success modal shows after assignment

### ✅ Functional Tests
- [ ] Can accept assignment on Notifications page
- [ ] Can decline assignment on Notifications page
- [ ] Assignment status changes after accepting/declining
- [ ] Notification disappears after reading
- [ ] Can assign multiple volunteers to same hazard

### ✅ Database Verification
```bash
# Check if notifications were created
python3 check_notifications.py

# Should show:
# - New notifications with is_alert: True
# - Assignment ID linked to notification
# - User ID of volunteer receiving notification
```

---

## Troubleshooting

### Problem: No notification badge appears
**Solution**: 
1. Check browser console (F12) for JavaScript errors
2. Verify `/api/notifications/unread-count` endpoint returns correct data
3. Try hard refresh: Ctrl+Shift+R or Cmd+Shift+R

### Problem: Volunteer doesn't see assignment
**Solution**:
1. Volunteer user should be within 50km of hazard (automatic filter)
2. Volunteer must have availability status set
3. Check database: `python3 check_notifications.py`
4. Try refreshing Notifications page manually

### Problem: Toast notification doesn't appear
**Solution**:
1. Toast is debounced (shows max once per 10 seconds)
2. Try assigning a different volunteer
3. Check browser console for errors
4. Verify Bootstrap is loaded correctly

### Problem: "Assign Volunteer" button doesn't work
**Solution**:
1. Check browser console (F12) for errors
2. Verify you're logged in as Official/Analyst/Admin
3. Make sure hazard and volunteer are selected
4. Try refreshing the page

---

## Advanced Testing

### Test 1: Multiple Simultaneous Assignments
```
1. Official creates 3 assignments in quick succession
2. Volunteer should see:
   - 3 separate notifications
   - Badge shows count 3
   - Toast appears 3 times (debounced)
```

### Test 2: Accept/Decline Flow
```
1. Volunteer receives assignment
2. Clicks "Accept" on Notifications page
3. Notification disappears
4. Check database: VolunteerAssignment.status = 'accepted'
5. Check database: Notification.is_read = True
```

### Test 3: Cross-Device Testing
```
1. Open app on two devices
2. Official on Device A
3. Volunteer on Device B
4. Assign on Device A
5. Check notification appears on Device B within 5 seconds
```

---

## Performance Notes

- Polling interval: **5 seconds** (can be adjusted in base.html)
- Toast debounce: **10 seconds** (prevent spam)
- Notifications page refresh: **3 seconds** (can be adjusted)
- Database queries: Minimal (single count query per poll)

---

## API Response Examples

### GET /api/notifications/unread-count
```json
{
  "count": 3
}
```

### GET /api/notifications
```json
[
  {
    "id": 226,
    "message": "You have been assigned to help with hazard: Test Emergency. Please accept or decline the assignment.",
    "report_id": null,
    "created_at": "2026-01-25T07:37:42.645661",
    "expires_at": null,
    "time_remaining": null
  }
]
```

### POST /api/coordination/assign-volunteer
```json
{
  "success": true,
  "message": "Volunteer assigned successfully",
  "assignment_id": 5,
  "distance_km": 0.0
}
```

---

## Contact & Support

If notifications still don't appear after following this guide:
1. Run `python3 check_notifications.py` to verify database state
2. Check browser console (F12) for JavaScript errors
3. Verify network requests in DevTools > Network tab
4. Look for 404 or 500 errors on API endpoints

---

**Last Updated**: January 25, 2026
**Tested On**: macOS with ngrok tunnel
**Status**: ✅ Ready for production testing
