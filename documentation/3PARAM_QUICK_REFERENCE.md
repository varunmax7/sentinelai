# 3-Parameter AI Accuracy Validation - Quick Reference

## What is It?
A system that validates disaster report accuracy using 3 independent parameters, each worth 33% of the final score.

## The 3 Parameters

```
┌─────────────────────────────────────────────────────────────┐
│              AI ACCURACY = 3 PARAMETERS                     │
├─────────────────────────────────────────────────────────────┤
│  Parameter 1: Weather & Early Warnings (Heatmap Match)     │
│  ↓                                                           │
│  Are there other reports confirming this hazard in this    │
│  area? (Searches 5.5km radius, past 24 hours)             │
│  Score: 50-95%                                             │
├─────────────────────────────────────────────────────────────┤
│  Parameter 2: Live Climate Data (Weather Alignment)        │
│  ↓                                                           │
│  Do current weather conditions support this hazard report? │
│  (Uses real-time Open-Meteo API data)                      │
│  Score: 45-90%                                             │
├─────────────────────────────────────────────────────────────┤
│  Parameter 3: User Quality (Credibility Score)             │
│  ↓                                                           │
│  How reliable is this user? (Role, track record, level)   │
│  Score: 17-95%                                             │
└─────────────────────────────────────────────────────────────┘
```

## Quick Examples

### ✅ High Accuracy Report (80%+)
**Scenario:** Official reports coastal flooding during high humidity
- Heatmap: 85% (4 similar reports nearby)
- Climate: 85% (Humidity 82%)
- User Quality: 95% (Official role, 90% approval rate)
- **Final: 88%** 🟢

### ⚠️ Medium Accuracy Report (60-79%)
**Scenario:** Regular user reports storm surge with moderate wind
- Heatmap: 70% (2 similar reports)
- Climate: 75% (Wind 22 km/h)
- User Quality: 65% (Citizen, 60% approval rate)
- **Final: 70%** 🟡

### 🔴 Low Accuracy Report (<40%)
**Scenario:** New user reports tsunami, no weather support
- Heatmap: 50% (No similar reports)
- Climate: 45% (Low wind speed)
- User Quality: 18% (New user, citizen, 0 approvals)
- **Final: 37%** 🔴

## Where to Find Results

### When Submitting a Report
```
Report submitted successfully!
AI Accuracy: 65% [Heatmap: 70% | Climate: 60% | User: 65%]
```

### In API Response
```json
GET /api/report/123/accuracy_3param
{
  "overall_accuracy_percent": 65,
  "parameter_1_heatmap": {"score_percent": 70, ...},
  "parameter_2_climate": {"score_percent": 60, ...},
  "parameter_3_user_quality": {"score_percent": 65, ...}
}
```

### In Dashboard
Each report shows the full breakdown with analysis text.

## How Each Parameter Works

### Parameter 1: Heatmap Match
**Question:** "Are others reporting the same hazard here?"
```
5+ reports     → 95% (Hotspot confirmed)
3-4 reports    → 85% (Strong cluster)
1-2 reports    → 70% (Some support)
0 reports      → 50% (Isolated report)
```

### Parameter 2: Climate Alignment
**Question:** "Does weather support this hazard?"
```
Storm Surge:
  Wind 25+ km/h  → 90% (Perfect match)
  Wind 15-25     → 75% (Reasonable)
  Wind <15       → 45% (Unlikely)

Flooding:
  Humidity 75%+  → 80% (Strong support)
  Humidity <75%  → 65% (Weak support)

High Waves:
  Wind 20+ or high humidity → 85% (Good support)
  Lower conditions         → 60% (Marginal)
```

### Parameter 3: User Quality
**Question:** "How trustworthy is this user?"
```
Official Role:       95% baseline
Analyst Role:        90% baseline
Agency:              88% baseline
Citizen:             50% baseline

+High approval rate: ×1.0 multiplier (80%+)
+Good approval rate: ×0.85 multiplier (60-79%)
+Low approval rate:  ×0.50 multiplier (<40%)
+New user:           ×0.60 multiplier

×User level factor: 0.7-1.0 (higher level = more trusted)
```

## Improving Your Accuracy Score

### To Improve Heatmap Match:
- Report hazards when others are also reporting them
- Be specific about location
- Use consistent hazard type classifications

### To Improve Climate Alignment:
- Report hazards when weather supports them
- Provide real-time observations
- Include weather conditions in description

### To Improve User Quality:
- Build track record by reporting accurately
- Your approved reports boost your credibility
- Higher user level increases trust
- Official/analyst roles get higher baseline

## Implementation Details

### Main Function
```python
from utils import validate_report_accuracy_3params

result = validate_report_accuracy_3params(report)
# Returns dict with all 3 parameters + overall score
```

### Integration
- ✅ Applied in `analyze_report_with_ai()` function
- ✅ New endpoint: `/api/report/<id>/accuracy_3param`
- ✅ Flash messages show breakdown on submit
- ✅ Dashboard displays all 3 parameters
- ✅ 50% weight to 3-param system, 50% to legacy analysis

## Testing

```bash
python test_3param_accuracy.py

# Output:
# 📊 OVERALL ACCURACY: 65%
# 📍 PARAMETER 1 (Heatmap): 70%
# 🌡️  PARAMETER 2 (Climate): 60%
# 👤 PARAMETER 3 (User Quality): 65%
```

## Accuracy Ranges

| Score | Interpretation | Color | Action |
|-------|---|---|---|
| 80-100% | Highly Reliable | 🟢 Green | Auto-approve, immediate alert |
| 60-79% | Good Confidence | 🟡 Yellow | Standard review |
| 40-59% | Questionable | 🟠 Orange | Needs verification |
| 0-39% | Low Confidence | 🔴 Red | Flag for investigation |

## API Endpoints

### Get 3-Parameter Breakdown
```
GET /api/report/<report_id>/accuracy_3param
Authorization: Bearer token
Response: JSON with all 3 parameter scores and analysis
```

## Files Modified

- ✅ `utils.py` - Added 4 new validation functions
- ✅ `app.py` - Updated AI analysis, added API endpoint
- ✅ `/report` route - Shows 3-param breakdown in flash message

## Key Points

- Each parameter is **independent** (doesn't affect others)
- Accuracy ranges from **0-100%**
- Real-time weather data from **Open-Meteo API**
- Heatmap checks **5.5km radius, 24 hours**
- User quality based on **approval history**
- **50% legacy + 50% 3-param** for final score (balanced approach)
