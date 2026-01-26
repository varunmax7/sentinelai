# 3-Parameter AI Accuracy Validation System

## Overview

The system now validates report accuracy using **3 key parameters**, each contributing 33% to the final accuracy score:

```
FINAL ACCURACY = (Parameter 1 × 33%) + (Parameter 2 × 33%) + (Parameter 3 × 34%)
```

---

## The 3 Parameters

### 📍 Parameter 1: Weather & Early Warnings - Heatmap Match (33%)

**What it checks:** Whether the reported hazard type is confirmed by other incident reports in the same area

**How it works:**
- Searches for similar hazards within 5.5 km radius
- Looks back 24 hours for corroborating reports
- Filters only **approved** and **pending** reports of the same hazard type

**Scoring:**
- **95%** → 5+ similar hazard reports (Strong hotspot confirmed)
- **85%** → 3-4 similar reports (Moderate hotspot)
- **70%** → 1-2 similar reports (Partial match)
- **50%** → No heatmap data (Plausible but unconfirmed)

**Example:**
```
Report: "Storm surge at Marina Beach"
Analysis: Found 3 other storm surge reports within 5km in last 24 hours
Score: 85% (Moderate heatmap confirmation)
```

---

### 🌡️ Parameter 2: Live Climate Data - Weather Alignment (33%)

**What it checks:** Whether current weather conditions support the reported hazard

**How it works:**
- Fetches real-time weather from Open-Meteo API (Free, no auth required)
- Analyzes temperature, humidity, and wind speed
- Matches weather conditions to hazard type expectations

**Scoring by Hazard Type:**

| Hazard Type | Supporting Conditions | Score |
|---|---|---|
| **Tsunami** | Usually seismic (not weather) | 75% |
| **Storm Surge** | Wind ≥25 km/h | 90% |
| **Storm Surge** | Wind 15-25 km/h | 75% |
| **Storm Surge** | Wind <15 km/h | 45% |
| **High Waves** | Wind ≥20 km/h OR Humidity ≥70% | 85% |
| **High Waves** | Lower winds/humidity | 60% |
| **Coastal Flooding** | Humidity ≥75% | 80% |
| **Abnormal Tide** | Any weather (inherent) | 70% |
| **Swell Surge** | Wind ≥15 km/h | 80% |

**Example:**
```
Report: "High waves at Goa Beach"
Current weather: Wind 28 km/h, Humidity 78%
Score: 85% (Strong wave conditions detected)
```

---

### 👤 Parameter 3: User Quality - Credibility Score (34%)

**What it checks:** User's historical accuracy and reliability

**How it works:**
- Evaluates user role (official > analyst > agency > citizen)
- Calculates report approval rate
- Considers user level and experience

**Base Score by Role:**
- **Official**: 95% baseline
- **Analyst**: 90% baseline
- **Agency**: 88% baseline
- **Citizen**: 50% baseline

**Historical Multiplier:**
- **80%+ approval rate**: 1.0× (Excellent track record)
- **60-79% approval rate**: 0.85× (Good track record)
- **40-59% approval rate**: 0.70× (Moderate track record)
- **<40% approval rate**: 0.50× (Low accuracy)
- **No reports yet**: 0.60× (New user penalty)

**Level Factor:**
- Scales from 0.7 to 1.0 based on user level (1-10)
- Higher level = more experience

**Final User Quality Score:**
```
Score = Base Role Score × History Multiplier × Level Factor
```

**Example:**
```
User: max (citizen, level 1)
Report history: 1 report submitted, 0 approved (0% approval rate)
Calculation:
  50% (citizen baseline) × 0.50 (low accuracy) × 0.70 (level 1)
  = 17.5% ≈ 18% Final Score
```

---

## Integration Points

### 1. **Report Submission** (`/report` endpoint)
When a user submits a report:
```python
ai_result = analyze_report_with_ai(report)
# Returns accuracy with 3-param breakdown
# Flash message shows: "AI Accuracy: 65% [Heatmap: 70% | Climate: 60% | User: 65%]"
```

### 2. **API Endpoint** - Get 3-Parameter Breakdown
```
GET /api/report/<report_id>/accuracy_3param
```

**Response:**
```json
{
  "report_id": 123,
  "title": "Storm Surge Warning",
  "overall_accuracy_percent": 65,
  "parameter_1_heatmap": {
    "name": "Weather & Early Warnings - Heatmap Match",
    "score_percent": 70,
    "analysis": "Strong heatmap confirmation: 4 similar reports detected",
    "weight": "33%"
  },
  "parameter_2_climate": {
    "name": "Live Climate Data - Weather Alignment",
    "score_percent": 60,
    "analysis": "Moderate wind conditions: 22km/h matches storm surge pattern",
    "weight": "33%"
  },
  "parameter_3_user_quality": {
    "name": "User Quality - Credibility Score",
    "score_percent": 65,
    "analysis": "Good track record: 8/10 reports approved (80%)",
    "weight": "34%",
    "user_role": "citizen",
    "user_level": 5,
    "user_total_reports": 10
  },
  "detailed_breakdown": "Heatmap Match: 70% | Climate Alignment: 60% | User Quality: 65%"
}
```

### 3. **Dashboard Integration**
Reports display full 3-parameter breakdown:
- Heatmap match percentage
- Current weather alignment
- User credibility score
- Combined accuracy

---

## How Accuracy Affects Reports

| Accuracy | Status | Action |
|----------|--------|--------|
| **80%+** | 🟢 High Confidence | Auto-approve, immediate alert |
| **60-79%** | 🟡 Moderate | Manual review queue |
| **40-59%** | 🟠 Low | Needs verification |
| **<40%** | 🔴 Very Low | Marked for investigation |

---

## Example Calculations

### Example 1: Official Reports Storm Surge
```
User: john (official, level 8)
Reports: 50 submitted, 48 approved (96%)

Parameter 1 (Heatmap): 85%
  - 4 similar storm surge reports in area
  
Parameter 2 (Climate): 88%
  - Wind 35 km/h (high winds support storm surge)
  
Parameter 3 (User Quality): 
  - Base: 95% (official)
  - Multiplier: 1.0 (96% approval rate)
  - Level: 0.84 (level 8)
  - Score: 95 × 1.0 × 0.84 = 79.8%

Final Accuracy: (85 + 88 + 80) / 3 = 84% ✅
```

### Example 2: New Citizen Reports Flooding
```
User: sarah (citizen, level 1)
Reports: 1 submitted, 0 approved (0%)

Parameter 1 (Heatmap): 50%
  - No similar flooding reports found
  
Parameter 2 (Climate): 78%
  - Humidity 82% supports flooding
  
Parameter 3 (User Quality):
  - Base: 50% (citizen)
  - Multiplier: 0.50 (new user, 0% approval)
  - Level: 0.70 (level 1)
  - Score: 50 × 0.50 × 0.70 = 17.5%

Final Accuracy: (50 + 78 + 18) / 3 = 49% ⚠️
```

---

## API Functions

### Main Function
```python
from utils import validate_report_accuracy_3params

result = validate_report_accuracy_3params(report)
# Returns: {
#   'overall_accuracy': 0.65,
#   'accuracy_percent': 65,
#   'parameter_1_heatmap': {...},
#   'parameter_2_climate': {...},
#   'parameter_3_user_quality': {...},
#   'detailed_analysis': "..."
# }
```

### Helper Functions
```python
_validate_heatmap_match(report, heatmap_data=None)
_validate_climate_alignment(report, weather_data=None)
_calculate_user_quality_score(user)
```

---

## Testing

Run the test script:
```bash
python test_3param_accuracy.py
```

**Test Output:**
```
📊 OVERALL ACCURACY: 65%
📍 PARAMETER 1 (Heatmap): 70%
🌡️  PARAMETER 2 (Climate): 60%
👤 PARAMETER 3 (User Quality): 65%
```

---

## Benefits

✅ **More Accurate Validation** - Uses multiple independent data sources
✅ **Fair to New Users** - Considers user history, not just role
✅ **Real-time Weather** - Validates against live climate conditions
✅ **Community Corroboration** - Heatmap confirms multiple reports
✅ **Transparent Scoring** - Users see exactly why accuracy is what it is
✅ **Actionable Feedback** - Shows what could improve the score

---

## Future Enhancements

- [ ] Machine learning model for hazard-weather matching
- [ ] Historical weather data for past events
- [ ] Social media sentiment analysis
- [ ] Satellite imagery validation
- [ ] User reputation score persistence
- [ ] Weighted adjustment based on hazard type priority
