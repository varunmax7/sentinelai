# Quick Testing Guide - Volunteer Assignment Notifications

## 🎯 Quick Test Steps

### 1️⃣ Open Browser Console
- Press **F12** (Windows/Linux) or **Cmd+Option+I** (Mac)
- Click on **Console** tab
- Keep it open during testing

### 2️⃣ Login as Coordinator
- Go to: http://localhost:5001/login
- Login with an account that has role: `official`, `analyst`, `admin`, or `coordinator`

### 3️⃣ Navigate to Volunteer Management
- Go to: http://localhost:5001/coordination/volunteers
- Click on **"Assign to Hazard"** tab

### 4️⃣ Select a Hazard
- Choose any hazard from the dropdown menu
- You should see a list of nearby volunteers appear

### 5️⃣ Assign a Volunteer
- Click the **"Assign Volunteer"** button
- Watch for:
  - ✅ Success modal popup
  - ✅ Console logs starting with `[FRONTEND]`
  - ✅ Terminal logs starting with `[ASSIGN]`

### 6️⃣ Check Volunteer's Notifications
- **Open a new browser tab** (or incognito window)
- Login as the volunteer user you just assigned
- Go to: http://localhost:5001/notifications
- You should see:
  - 📬 A new notification with the hazard name
  - ✅ Green checkmark button (Accept)
  - ❌ Red X button (Decline)

### 7️⃣ Test Accept/Decline
- Click **Accept** (green checkmark) OR **Decline** (red X)
- The notification should disappear
- Go back to the coordinator account
- Check notifications - you should see a response notification

## 🔍 What to Look For

### In Browser Console (Coordinator):
```
[FRONTEND] Starting assignment: vol=1, hazard=2, type=emergency
[FRONTEND] Sending payload: {...}
[FRONTEND] Response status: 200 {...}
[FRONTEND] ✓ Assignment successful!
[FRONTEND] ✓ Notification ID: 12
[FRONTEND] ✓ Volunteer: varunmax7
[FRONTEND] ✓ Assignment ID: 5
```

### In Terminal (Backend):
```
[ASSIGN] Received request: volunteer_id=1, hazard_id=2, type=emergency
[ASSIGN] Found volunteer: 1, user_id=3
[ASSIGN] Found hazard: Tsunami Warning (type=emergency)
[ASSIGN] Distance calculated: 5.23km
[ASSIGN] Created assignment: id=5, status=pending
[ASSIGN] ✓ Notification created: id=12, user=varunmax7
[ASSIGN] ✓ Assignment complete! Notification sent to varunmax7
```

### In Volunteer's Notifications Page:
```
🔔 You have been assigned to help with hazard: [Hazard Name]. 
   Please accept or decline the assignment.
   
   [✓ Accept]  [✗ Decline]
```

## ❗ Common Issues

### Issue: "No volunteers found"
**Solution**: Make sure volunteers are registered and within 50km of the hazard

### Issue: "Volunteer already assigned"
**Solution**: The volunteer is already assigned to this hazard. Choose a different volunteer or hazard.

### Issue: No notification appears
**Solution**: 
1. Check terminal logs - is notification being created?
2. Check browser console - any errors?
3. Make sure you're logged in as the correct volunteer user
4. Try clicking "Show All" in notifications page

## 📊 Test Scenarios

### Scenario 1: Happy Path
1. Coordinator assigns volunteer → ✅ Success
2. Volunteer receives notification → ✅ Success
3. Volunteer accepts → ✅ Success
4. Coordinator receives acceptance notification → ✅ Success

### Scenario 2: Decline Path
1. Coordinator assigns volunteer → ✅ Success
2. Volunteer receives notification → ✅ Success
3. Volunteer declines → ✅ Success
4. Coordinator receives decline notification → ✅ Success

### Scenario 3: Multiple Assignments
1. Assign volunteer to Hazard A → ✅ Success
2. Try to assign same volunteer to Hazard A again → ❌ Error (expected)
3. Assign same volunteer to Hazard B → ✅ Success

## 🎬 Video Recording Tip
If you want to record the test:
1. Use browser's built-in screen recording
2. Or use OBS Studio / QuickTime (Mac)
3. Show both the coordinator view and volunteer view side-by-side

## 📝 Notes
- Notifications are real-time (no page refresh needed)
- Accept/Decline buttons only appear for assignment notifications
- The notification message must contain "been assigned" to show buttons
- Volunteers must be within 50km to be assigned
- Volunteers must be within 500m to complete the rescue
