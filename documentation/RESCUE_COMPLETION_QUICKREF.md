# Rescue Completion System - Quick Reference

## ⚡ Quick Start for Volunteers

### How to Complete a Rescue:

1. **Accept Assignment** 
   - Go to Notifications
   - Click ✓ Accept on assignment notification

2. **Go to Hazard Location**
   - Use GPS on your phone
   - Must be within 500m of hazard

3. **Click "Complete Rescue"**
   - System verifies your location
   - GPS must show you at/near hazard

4. **Upload Photo Proof**
   - Take photo of rescue
   - Upload via drag-and-drop or click
   - Max 5MB, PNG/JPG/GIF

5. **Add Notes (Optional)**
   - Describe what was done
   - Mention any challenges
   - Note victim status

6. **Submit & Earn Points!**
   - Points instantly added
   - Official receives notification
   - Your rank updates

### Points You'll Earn:

| Level | Base Points | Speed Bonus (if <24hrs) | Max Total |
|-------|------------|------------------------|-----------|
| **Beginner** | 100 | +30 | 130 |
| **Intermediate** | 150 | +30 | 180 |
| **Expert** | 200 | +30 | 230 |

**Example**: Expert completes in 4 hours = 200 + 30 = **230 points** 🏆

---

## 📊 Leaderboard

### Access
- Path: **http://yoursite/leaderboard**
- Shows top 50 volunteers per page

### What You'll See:

1. **Your Rank** (if logged in as volunteer)
   - 🥇 Your current position
   - Points earned
   - Rescues completed

2. **Top Volunteers**
   - Rank badges (🥇🥈🥉)
   - Username & experience level
   - Points & rescue count
   - Verified badge ✓

### Sorting
- Ranked by total points (highest first)
- Ties broken by rescue count
- Then by join date

---

## 🔧 For Developers

### Database Tables Modified:

**volunteers**:
```sql
ALTER TABLE volunteers ADD COLUMN points INTEGER DEFAULT 0;
ALTER TABLE volunteers ADD COLUMN total_rescues INTEGER DEFAULT 0;
```

**volunteer_assignments**:
```sql
ALTER TABLE volunteer_assignments ADD COLUMN completion_photo VARCHAR(500);
ALTER TABLE volunteer_assignments ADD COLUMN completion_notes TEXT;
ALTER TABLE volunteer_assignments ADD COLUMN points_earned INTEGER DEFAULT 0;
```

### API Endpoints:

```bash
# Complete a rescue
POST /api/coordination/assignment/{id}/complete
{
  "photo_url": "https://...",
  "notes": "Rescue successful",
  "latitude": 40.7128,
  "longitude": -74.0060
}

# Get leaderboard
GET /api/leaderboard?page=1&per_page=50

# Get your rank
GET /api/leaderboard/user/{user_id}
```

### Routes:

```
GET /rescue-complete?assignment_id={id}   → Completion form
GET /leaderboard                          → Leaderboard page
```

---

## 🎮 Test Scenario

### Setup:
1. Create 2 accounts: Official + Volunteer
2. Official creates Emergency Event at coordinates (40.7128, -74.0060)
3. Volunteer registers at location within 50km

### Test Flow:
```
1. Official assigns volunteer to event
2. Volunteer receives notification
3. Volunteer clicks ✓ Accept
4. Volunteer visits /rescue-complete?assignment_id=X
5. GPS shows location (must mock to be within 500m)
6. Volunteer uploads photo
7. Volunteer submits
8. Points awarded (100-230 depending on level)
9. Check /leaderboard - volunteer appears!
```

---

## ⚙️ Configuration

### Point Values
Edit in `/app.py` function `complete_rescue_assignment()`:
```python
base_points = 100  # Change base
if volunteer.experience_level == 'intermediate':
    points_earned = int(base_points * 1.5)  # 150
elif volunteer.experience_level == 'expert':
    points_earned = int(base_points * 2)    # 200
```

### Distance Requirement
Edit in `/app.py`:
```python
if distance_at_completion > 0.5:  # 0.5 km = 500m
    # Reject - too far
```

Change `0.5` to any value in km.

### Speed Bonus Calculation
Edit in `/app.py`:
```python
if hours_taken < 24:  # Change 24 to other hour value
    bonus_points = int((24 - hours_taken) / 4)  # Adjust divisor
```

---

## 📸 Photo Upload

### File Requirements:
- **Max Size**: 5MB
- **Formats**: PNG, JPG, GIF
- **Auto-resizing**: Not implemented (use client-side)

### Storage:
- Photos stored in `/static/uploads/`
- Filename: Auto-generated unique ID
- URL saved in DB

---

## 🚨 Common Issues

### "You are X km away"
- Solution: Move closer to hazard location (within 500m)
- Accuracy: ±10-30m depending on GPS signal

### Photo won't upload
- Check file size < 5MB
- Check file format (PNG/JPG/GIF)
- Check browser permissions for file access

### No points awarded
- Check: Assignment was "accepted" status
- Check: You're the assigned volunteer
- Check: Within 500m of location
- Check: Photo uploaded successfully

---

## 📱 Mobile Tips

- Use mobile's GPS for accurate location
- Connect to internet for photo upload
- Allow location permission when requested
- Check signal strength for GPS accuracy

---

## 📞 Support

For issues, check:
1. Database migration applied: `flask db upgrade`
2. GPS coordinates valid (latitude -90 to 90, longitude -180 to 180)
3. Browser console for JavaScript errors
4. Server logs for API errors

