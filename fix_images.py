import os
import re
from app import app, db
from models import Report

# Get list of actual files in uploads
upload_dir = "/Users/ramavathvarun/Downloads/disaster_management/static/uploads"
files = os.listdir(upload_dir)
image_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]

print(f"Found {len(image_files)} image files in filesystem")

# Create a mapping of base names to actual filenames
file_map = {}
for filename in image_files:
    # Extract base name without timestamps added by macOS
    # e.g., "captured_photo_20250921_135934 11.10.22 AM.jpg" -> "captured_photo_20250921_135934.jpg"
    match = re.search(r'([a-zA-Z0-9_]+\.jpg)', filename)
    if match:
        base_name = match.group(1)
        file_map[base_name] = filename

print(f"Created mapping with {len(file_map)} entries")

# Update database
with app.app_context():
    reports = Report.query.filter(Report.image_file.isnot(None)).all()
    updated = 0
    
    for report in reports:
        old_name = report.image_file
        # Check if there's a mapping for this file
        if old_name in file_map:
            # File still exists with timestamp
            new_name = file_map[old_name]
            # Don't update if already correct
            if report.image_file != new_name:
                report.image_file = new_name
                updated += 1
                print(f"Report #{report.id}: {old_name} -> {new_name}")
        else:
            # Check if actual file exists
            actual_path = os.path.join(upload_dir, old_name)
            if not os.path.exists(actual_path):
                # Try to find it with timestamp pattern
                for actual_file in image_files:
                    if old_name.replace('.jpg', '') in actual_file:
                        report.image_file = actual_file
                        updated += 1
                        print(f"Report #{report.id}: {old_name} -> {actual_file}")
                        break
    
    if updated > 0:
        db.session.commit()
        print(f"Updated {updated} reports in database")
    else:
        print("No updates needed")
