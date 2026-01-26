# Rescue Completion System - Architecture & Data Flow

## System Overview

The rescue completion system allows volunteers to mark emergency rescues as complete by:
1. Providing location verification (GPS within 500m of hazard)
2. Uploading photo proof
3. Adding rescue notes
4. Earning points based on experience level and completion speed
5. Appearing on volunteer leaderboard

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        VOLUNTEER                                │
│                    (Mobile/Desktop)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
        ┌───────────▼────────────┐  ┌──▼──────────────────┐
        │ Browser Geolocation    │  │ Photo File Upload   │
        │ API                    │  │                     │
        │                        │  │ - Max 5MB           │
        │ - Gets GPS coords      │  │ - JPEG/PNG/GIF/WebP │
        │ - Updates every 5s     │  │ - Drag-drop support │
        └───────────┬────────────┘  └──┬──────────────────┘
                    │                   │
                    │   ┌───────────────┴─────────────────┐
                    │   │                                 │
        ┌───────────▼───▼──────────────────────────────────┐
        │     rescue_completion.html                       │
        │  (Client-Side Validation & Display)              │
        │                                                  │
        │  - Real-time distance calculation (JS)          │
        │  - Haversine formula in browser                 │
        │  - Location status indicator                    │
        │  - Form enable/disable based on distance        │
        │  - Photo preview                                │
        │  - Points preview calculation                   │
        └───────────────┬──────────────────────────────────┘
                        │
        ┌───────────────▼──────────────────────────┐
        │   Form Submission                        │
        │ POST /api/coordination/assignment/       │
        │      {id}/complete                       │
        │                                          │
        │  Payload:                               │
        │  {                                       │
        │    photo_url: "...",                    │
        │    notes: "...",                        │
        │    latitude: 40.7128,                   │
        │    longitude: -74.0060                  │
        │  }                                       │
        └───────────────┬──────────────────────────┘
                        │
        ┌───────────────▼──────────────────────────┐
        │      Flask Backend (app.py)              │
        │                                          │
        │  complete_rescue_assignment()            │
        │                                          │
        │  1. Authenticate user                   │
        │  2. Validate assignment exists           │
        │  3. Verify is assigned volunteer         │
        │  4. Check status = "accepted"            │
        │  5. Get hazard location                  │
        │  6. Calculate distance (Haversine)      │
        │  7. Validate ≤ 500m distance            │
        │  8. Calculate points earned              │
        │  9. Update volunteer stats               │
        │  10. Send notification                   │
        │  11. Return success response             │
        └───────────────┬──────────────────────────┘
                        │
        ┌───────────────▼──────────────────────────┐
        │      Database Updates                    │
        │                                          │
        │  volunteer_assignments:                 │
        │  - status: "completed"                   │
        │  - completed_at: datetime.utcnow()      │
        │  - completion_photo: photo_url          │
        │  - completion_notes: notes              │
        │  - points_earned: calculated            │
        │                                          │
        │  volunteers:                            │
        │  - points += calculated                 │
        │  - total_rescues += 1                   │
        │                                          │
        │  notifications:                         │
        │  - New notification to assigner         │
        └───────────────┬──────────────────────────┘
                        │
        ┌───────────────▼──────────────────────────┐
        │   Response to Client                     │
        │                                          │
        │  {                                       │
        │    success: true,                        │
        │    points_earned: 225,                   │
        │    total_points: 450,                    │
        │    total_rescues: 3                      │
        │  }                                       │
        └───────────────┬──────────────────────────┘
                        │
        ┌───────────────▼──────────────────────────┐
        │   Leaderboard Update                     │
        │                                          │
        │  GET /api/leaderboard                    │
        │                                          │
        │  Returns volunteers ranked by:          │
        │  1. Points (descending)                  │
        │  2. Rescue count (descending)            │
        │  3. Creation date (ascending)            │
        └───────────────────────────────────────────┘
```

---

## Data Model

### Volunteer Table
```
volunteers
├── id (PK)
├── user_id (FK)
├── skills
├── availability
├── experience_level (beginner/intermediate/expert)
├── certifications
├── location
├── latitude
├── longitude
├── is_verified
├── created_at
├── points ★ (NEW)              ← Cumulative points from all rescues
└── total_rescues ★ (NEW)       ← Count of completed rescues
```

### VolunteerAssignment Table
```
volunteer_assignments
├── id (PK)
├── volunteer_id (FK → volunteers)
├── emergency_event_id (FK)
├── role
├── status (pending/accepted/deployed/completed/declined)
├── assigned_by (FK → users)
├── assigned_at
├── accepted_at
├── completed_at
├── distance_km (distance at time of assignment)
├── completion_photo ★ (NEW)    ← URL/path to proof photo
├── completion_notes ★ (NEW)    ← Volunteer's notes about rescue
└── points_earned ★ (NEW)       ← Points awarded for this rescue
```

### Notification Table (Updated)
```
notifications
├── id (PK)
├── user_id (FK)
├── message (includes: "{volunteer} completed {hazard}. Earned {points} points.")
├── is_alert
├── created_at
└── read_at (optional)
```

---

## Points Calculation Algorithm

```
┌─────────────────────────────────────────┐
│  Retrieve Volunteer Experience Level    │
└──────────────┬──────────────────────────┘
               │
        ┌──────▼─────────┐
        │                │
   ┌────▼────┐    ┌──────▼──────┐    ┌──────▼──────┐
   │ Beginner │    │Intermediate │    │   Expert    │
   └────┬────┘    └──────┬──────┘    └──────┬──────┘
        │                │                  │
    base=100         base=150            base=200
        │                │                  │
        └────────────────┬──────────────────┘
                         │
        ┌────────────────▼──────────────────┐
        │  Get Assignment accepted_at Time  │
        │  Calculate Hours Since Acceptance │
        └────────────────┬──────────────────┘
                         │
                ┌────────▼────────┐
                │                 │
           ┌────▼─────┐    ┌──────▼────┐
           │ < 24h    │    │ ≥ 24h      │
           │          │    │            │
           └────┬─────┘    └──────┬─────┘
                │                 │
        ┌───────▼────────┐   ┌────▼────────┐
        │ bonus = (24 -  │   │ bonus = 0   │
        │  hours) / 4    │   │             │
        │ (max 30)       │   └────┬────────┘
        └───────┬────────┘        │
                │                 │
                └─────────┬───────┘
                          │
            ┌─────────────▼──────────────┐
            │ points_earned = base +     │
            │                 bonus      │
            │                            │
            │ Result: 100-230 points     │
            └────────────────────────────┘
```

### Examples:
```
Example 1: Beginner, 4 hours after accepting
- Base: 100
- Hours taken: 4
- Bonus: (24 - 4) / 4 = 5 points
- Total: 100 + 5 = 105 points

Example 2: Intermediate, 10 hours after accepting
- Base: 150
- Hours taken: 10
- Bonus: (24 - 10) / 4 = 3.5 → 3 points (rounded down)
- Total: 150 + 3 = 153 points

Example 3: Expert, 1 hour after accepting
- Base: 200
- Hours taken: 1
- Bonus: (24 - 1) / 4 = 5.75 → 5 points (rounded down)
- Total: 200 + 5 = 205 points

Example 4: Beginner, 24+ hours after accepting
- Base: 100
- Hours taken: 36
- Bonus: 0 (no bonus for >24h)
- Total: 100 points
```

---

## Distance Verification Algorithm

```
┌──────────────────────────────┐
│  Get Hazard Location         │
│  from Database               │
│  (lat1, lon1)               │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│  Get Volunteer GPS           │
│  from Browser Geolocation    │
│  (lat2, lon2)               │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────────────────┐
│  Haversine Formula                       │
│                                          │
│  Δσ = 2 * arcsin(√[sin²(Δφ/2) +        │
│        cos(φ1) * cos(φ2) * sin²(Δλ/2)]) │
│                                          │
│  d = R * Δσ  (R = 6371 km)              │
└──────────────┬───────────────────────────┘
               │
        ┌──────▼──────┐
        │              │
   ┌────▼─────┐  ┌────▼──────┐
   │ ≤ 0.5 km │  │ > 0.5 km  │
   │ (500m)   │  │           │
   └────┬─────┘  └────┬──────┘
        │             │
    ✓ PASS       ✗ FAIL
  Allow submit   Reject
        │             │
        └─────┬───────┘
              │
        ┌─────▼────────────┐
        │ Enable/Disable   │
        │ Submit Button    │
        │                  │
        │ & Show Distance  │
        │ Status           │
        └──────────────────┘
```

---

## Request/Response Flow

### 1. Rescue Completion Request

**Request:**
```http
POST /api/coordination/assignment/1/complete HTTP/1.1
Content-Type: application/json
Authorization: Bearer <token>

{
  "photo_url": "https://cdn.example.com/rescue_photo_12345.jpg",
  "notes": "Successfully rescued 2 people from building. Minor injuries treated.",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Validation Steps:**
1. ✓ User authenticated
2. ✓ Assignment exists
3. ✓ User is assigned volunteer
4. ✓ Assignment status = "accepted"
5. ✓ Photo URL provided
6. ✓ Coordinates provided
7. ✓ Distance ≤ 500m
8. ✓ All checks pass → Process

**Success Response:**
```json
{
  "success": true,
  "message": "Rescue completed successfully!",
  "assignment_id": 1,
  "points_earned": 225,
  "total_points": 450,
  "total_rescues": 3
}
```

**Error Responses:**
```json
// Missing photo
{
  "error": "Photo proof is required"
}

// Too far from hazard
{
  "error": "You are 1.23km away from the hazard location. You must be within 500m to complete.",
  "required_distance_km": 0.5,
  "current_distance_km": 1.23
}

// Wrong assignment status
{
  "error": "Only accepted assignments can be completed"
}

// Unauthorized user
{
  "error": "Unauthorized"
}
```

### 2. Leaderboard Request

**Request:**
```http
GET /api/leaderboard?page=1&per_page=50 HTTP/1.1
Authorization: Bearer <token>
```

**Response:**
```json
{
  "leaderboard": [
    {
      "rank": 1,
      "user_id": 5,
      "username": "john_expert",
      "points": 685,
      "rescues": 4,
      "experience": "expert",
      "is_verified": true
    },
    {
      "rank": 2,
      "user_id": 8,
      "username": "jane_intermediate",
      "points": 453,
      "rescues": 3,
      "experience": "intermediate",
      "is_verified": true
    },
    {
      "rank": 3,
      "user_id": 12,
      "username": "bob_beginner",
      "points": 210,
      "rescues": 2,
      "experience": "beginner",
      "is_verified": true
    }
  ],
  "total": 42,
  "pages": 1,
  "current_page": 1
}
```

### 3. User Rank Request

**Request:**
```http
GET /api/leaderboard/user/5 HTTP/1.1
Authorization: Bearer <token>
```

**Response:**
```json
{
  "user_id": 5,
  "username": "john_expert",
  "rank": 1,
  "points": 685,
  "rescues": 4,
  "experience": "expert",
  "is_verified": true
}
```

---

## Database Transaction Flow

```
┌─ BEGIN TRANSACTION ─────────────────┐
│                                      │
│  1. Validate all inputs             │
│     (User, assignment, photo, GPS)  │
│                                      │
│  2. Update VolunteerAssignment      │
│     - status = "completed"          │
│     - completed_at = NOW()          │
│     - completion_photo = URL        │
│     - completion_notes = text       │
│     - points_earned = calculated    │
│                                      │
│  3. Update Volunteer                │
│     - points += calculated          │
│     - total_rescues += 1            │
│                                      │
│  4. Create Notification             │
│     - For the assignment creator    │
│     - Message with completion info  │
│                                      │
│  5. COMMIT all changes              │
│                                      │
└─ END TRANSACTION ──────────────────┘
        │
        └─ On Error: ROLLBACK all changes
```

---

## Integration with Existing Systems

### Assignment System (Phase 6)
```
Assignment Flow:
1. Emergency created
2. Volunteer assigned → status = "pending"
3. Volunteer accepts → status = "accepted" ← Entry point for Phase 7
4. Volunteer completes rescue → (Phase 7)
   - Verification form displayed
   - Photo + GPS collected
   - Points calculated
   - Status = "completed"
   - Points awarded
5. Leaderboard updated
```

### Notification System
```
Notification Events:
- Assignment created → "New rescue assignment"
- Assignment accepted → "Volunteer accepted"
- Assignment completed → "Rescue completed! {user} earned {points} points."
```

### User Authentication
```
- All endpoints require @login_required
- Verify user is assigned volunteer
- Prevent unauthorized access
```

### Database Access
```
- Flask-SQLAlchemy ORM
- Automatic connection pooling
- Transaction management
- Migration support via Alembic
```

---

## Performance Considerations

### Query Optimization
```
Leaderboard Query:
SELECT * FROM volunteers
  ORDER BY points DESC, total_rescues DESC, created_at ASC
  LIMIT 50 OFFSET 0

Indexes recommended:
- volunteers(points DESC)
- volunteers(total_rescues DESC)
```

### Caching Opportunities
```
- Cache leaderboard for 5-minute TTL
- Cache user rank for 1-minute TTL
- Invalidate on points update
```

### Scalability Limits
```
Current architecture supports:
- 10,000+ volunteers
- 100,000+ rescues
- Real-time leaderboard updates

Future improvements:
- Redis caching layer
- Asynchronous notification processing
- Microservice for points calculation
```

---

## Security Considerations

### Input Validation
```
✓ Photo URL validation
✓ GPS coordinate bounds checking
✓ Assignment ID validation
✓ User authorization checks
✓ Status state validation
```

### Authorization
```
✓ Login required on all endpoints
✓ Verify user is assigned volunteer
✓ Prevent cross-user access
✓ Assignment creator notification only
```

### Data Protection
```
✓ GPS coordinates stored securely
✓ Photo URLs validated
✓ SQL injection prevention (ORM)
✓ CSRF protection via Flask-WTF
```

### Potential Vulnerabilities
```
⚠ GPS spoofing: Could provide fake coordinates
   Mitigation: Server-side validation against hazard location
   
⚠ Photo forgery: Could upload unrelated photos
   Mitigation: AI-based image verification (future)
   
⚠ Points farming: Multiple rapid rescues
   Mitigation: Time delays between assignments
   
⚠ Timezone issues: Different volunteer timezones
   Mitigation: Use UTC throughout system
```

---

## Monitoring & Logging

### Key Metrics to Track
```
- Rescue completion rate
- Average points earned per rescue
- Leaderboard churn (rank changes)
- Photo upload success rate
- GPS accuracy issues
- API response times
```

### Error Scenarios to Log
```
- Distance validation failures
- Photo upload errors
- GPS timeout/unavailable
- Database transaction failures
- Authorization failures
```

---

## Future Enhancements

```
1. Real-time leaderboard updates (WebSocket)
2. Achievements/badges system
3. Team-based scoring
4. Seasonal leaderboards
5. Photo verification with ML
6. Offline-first support
7. Volunteer matching algorithm
8. Analytics dashboard
9. Export/reporting features
10. Integration with external APIs
```

---

**Architecture Document Complete** ✓
