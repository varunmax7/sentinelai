# Volunteering System - Quick Reference Guide

## For Users (Volunteers)

### How to Register as a Volunteer
1. Go to your Dashboard
2. Click the green **"Be a Volunteer"** button (top right, under toolbar)
3. Fill out the volunteer form:
   - **Skills & Expertise**: List your skills (required)
   - **Experience Level**: Select your level (required)
   - **Certifications**: Add any relevant certifications (optional)
   - **Location**: Your current location (will auto-fill with GPS if you allow)
   - **Availability**: Are you available, busy, or unavailable? (required)
4. Click **"Register as Volunteer"**
5. ✅ You're now in the volunteer pool!

### How to Respond to Assignment
1. You'll receive a notification: "You have been assigned to help with hazard: {HAZARD_NAME}"
2. Click the notification to view details
3. Choose to:
   - **Accept**: You're ready to help with this hazard
   - **Decline**: You're not available for this hazard
4. The official who assigned you will be notified of your response

### Check Your Status
- Visit **Volunteer Management** to see:
  - Your current status (Available/Assigned/Unavailable)
  - What hazard you're assigned to
  - Your assigned distance from hazard location

---

## For Officials/Analysts (Coordinators)

### How to Assign Volunteers to a Hazard

#### Step 1: Go to Volunteer Management
- Click **Coordination** → **Volunteer Management**

#### Step 2: Click "Assign to Hazard" Tab
- This is the second tab in the Volunteer Management page

#### Step 3: Select a Hazard
- Click the dropdown: **"Select a hazard to view nearby volunteers"**
- Choose the hazard/emergency you need help with

#### Step 4: See Nearby Volunteers (50km Filter)
- The system automatically shows:
  - Only available volunteers
  - Only within 50km of the hazard
  - Sorted by distance (closest first)
  
- For each volunteer, you'll see:
  - Name
  - Distance in km
  - Experience level
  - Verification status
  - Skills preview

#### Step 5: Assign Volunteer
- Click the green **"Assign"** button next to the volunteer's name
- ✅ Assignment sent! Volunteer receives notification

#### Step 6: Wait for Response
- You'll receive notification when volunteer accepts/declines
- Once accepted, they appear on the hazard feed

### What the 50km Filter Does
- **Maximum Distance**: Volunteers must be within 50km of hazard location
- **Prevents**: Assigning volunteers who are too far away
- **Shows**: Real distance in kilometers for each volunteer
- **Filters**: Only shows available, verified volunteers with location data

### Key Information on Volunteer Management
- **Total Volunteers**: All volunteers in system
- **Available**: Volunteers ready to be assigned
- **Assigned**: Volunteers currently working on hazards
- **Trained**: Volunteers with verified certifications

---

## Key Features Overview

| Feature | User | Official |
|---------|------|----------|
| Register as Volunteer | ✅ | - |
| Auto-Location Detection | ✅ | - |
| View Assignments | ✅ | ✅ |
| Accept/Decline Assignment | ✅ | - |
| See All Volunteers | - | ✅ |
| Assign to Hazard | - | ✅ |
| 50km Proximity Filter | - | ✅ |
| Get Notifications | ✅ | ✅ |
| See Volunteer Count on Hazard | ✅ | ✅ |

---

## Assignment Status Flow

```
Official Assigns
       ↓
   PENDING (waiting for volunteer response)
       ↓
   ┌───┴───┐
   ↓       ↓
ACCEPTED  DECLINED
   ↓
DEPLOYED (working on hazard)
   ↓
COMPLETED (finished)
```

---

## FAQ

### Q: What if my location permission is denied?
A: You can manually enter your location in the text field. The auto-fill is just for convenience.

### Q: Can I change my availability status?
A: Not yet, but this feature is coming. For now, contact an official.

### Q: What if I'm assigned to multiple hazards?
A: Currently, you can only be actively working on one hazard. Finish or decline the current one first.

### Q: How do I know my distance from a hazard?
A: When viewing volunteers for a hazard, the distance is shown next to each volunteer's name (e.g., "3.5km away").

### Q: What if there are no volunteers within 50km?
A: The system will show: "No available volunteers within 50km of the selected hazard." Officials may need to expand search radius or recruit more volunteers.

### Q: Can I see who else is assigned to my hazard?
A: Yes! The hazard feed post shows all assigned volunteers with badges.

### Q: Do I get paid to volunteer?
A: That's determined by your agency's policies. This system just coordinates availability and assignments.

---

## Distance Calculation

The system uses GPS coordinates to calculate distance:
- **Method**: Haversine formula (great-circle distance)
- **Accuracy**: Within ±50-500 meters in real-world conditions
- **Maximum Assignment Distance**: 50km
- **Why 50km**: Balances response time with volunteer pool size

---

## Notification Types

### For Volunteers
- "You have been assigned to hazard: {NAME}"
- "Assignment for {HAZARD} accepted successfully"

### For Officials  
- "{VOLUNTEER_NAME} has accepted assignment for {HAZARD}"
- "{VOLUNTEER_NAME} has declined assignment for {HAZARD}"

---

## Troubleshooting

### Issue: "Be a Volunteer" button not showing
- **Check**: You're logged in
- **Check**: You don't already have a volunteer profile
- **Contact**: Your system administrator

### Issue: No volunteers showing within 50km
- **Reason 1**: No volunteers have registered
- **Reason 2**: All volunteers are >50km away
- **Solution**: Ask more volunteers to register or expand the radius (future feature)

### Issue: Location not auto-filling
- **Reason**: Browser permission denied or location unavailable
- **Solution**: Manually enter your location in the text field
- **Note**: This is normal - just type your address

### Issue: Assignment not sending
- **Check**: Internet connection
- **Check**: Volunteer has valid GPS coordinates
- **Check**: Distance is ≤50km
- **Try**: Refresh page and try again

---

## Version
- **Version**: 1.0
- **Released**: January 24, 2026
- **Status**: Production Ready

---

## Support
For technical issues or feature requests, contact your disaster management coordinator.
