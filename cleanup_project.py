"""
Project Cleanup Script - Removes unnecessary markdown files
Backs up files before deletion and organizes the project
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

# Create backup and archive directories
backup_dir = Path("_BACKUP_BEFORE_CLEANUP")
archive_dir = Path("_ARCHIVED_DOCS")
backup_dir.mkdir(exist_ok=True)
archive_dir.mkdir(exist_ok=True)

print("=" * 80)
print("PROJECT CLEANUP - MARKDOWN FILES")
print("=" * 80)
print()

# Files to KEEP (essential documentation)
KEEP_FILES = {
    "README.md",                           # Main project readme
    "hackathon-0.md",                      # Original requirements
    "FINAL_IMPLEMENTATION_SUMMARY.md",     # Most recent comprehensive guide
    "SYSTEM_DIAGNOSIS_REPORT.md",          # Diagnostic information
    "COMPLETE_FIX_REPORT.md",              # Implementation details
    "SECURITY_WARNING.md",                 # Security information
    "COMPLETE_USAGE_GUIDE.md",             # Usage instructions
}

# Patterns to DELETE (redundant/outdated)
DELETE_PATTERNS = [
    # Old completion reports
    "Bronze_Tier_Completion_Report.md",
    "Silver_Tier_Completion_Report.md",
    "Bronze_Tier_Verification_Report.md",
    "Silver_Tier_Report.md",

    # Duplicate guides
    "BRONZE_TIER_COMPLETION_GUIDE.md",
    "COMPLETE_IMPLEMENTATION_GUIDE.md",
    "INTEGRATION_SETUP_GUIDE.md",
    "MANUAL_TESTING_GUIDE.md",
    "SILVER_TIER_TESTING_GUIDE.md",

    # Multiple final reports (keep only FINAL_IMPLEMENTATION_SUMMARY.md)
    "FINAL_STATUS_REPORT.md",
    "FINAL_SUBMISSION_GUIDE.md",
    "FINAL_SUMMARY.md",
    "FINAL_CAPABILITIES_SUMMARY.md",
    "IMPLEMENTATION_SUMMARY.md",

    # Duplicate submission docs
    "SUBMISSION_CHECKLIST.md",
    "SUBMISSION_READY.md",
    "READY_TO_SUBMIT.md",
    "README_HACKATHON.md",

    # Demo files
    "DEMO_BRONZE_TIER.md",
    "DEMO_GOLD_TIER.md",
    "DEMO_PLATINUM_TIER.md",
    "DEMO_SILVER_TIER.md",
    "COMPLETE_WORKFLOW_DEMO.md",

    # Duplicate status reports
    "SILVER_TIER_STATUS.md",
    "SILVER_TIER_SUMMARY.md",
    "COMPLETE_HACKATHON_STATUS.md",
    "ALL_TIERS_TESTING_COMPLETE.md",

    # Duplicate tier docs
    "GOLD_TIER_COMPLETE.md",
    "GOLD_TIER_PLAN.md",
    "GOLD_TIER_README.md",
    "PLATINUM_TIER_PLAN.md",
    "PLATINUM_TIER_README.md",

    # Duplicate start guides
    "START_HERE.md",
    "START_NOW.md",
    "QUICK_START.md",
    "HOW_TO_RUN_BRONZE_TIER.md",

    # Other duplicates
    "ACTION_PLAN.md",
    "CEO_Briefing.md",
    "COMPLETE_TEST_REPORT.md",
    "CONDITIONS_GUIDE.md",
    "HACKATHON_REQUIREMENTS_ANALYSIS.md",
    "INTEGRATION_COMPLETE.md",
    "MASTER_SUMMARY_REPORT.md",
    "TERMINAL_OUTPUT_SPECIFICATIONS.md",
    "TIER_PROGRESSION_ROADMAP.md",
    "TIER_SCORING_AND_CLEANUP_REPORT.md",
    "WHATSAPP_WATCHER_EXPLAINED.md",
    "BRONZE_TIER_FINAL_VERIFICATION.md",
    "BRONZE_TIER_SUBMISSION_CHECKLIST.md",
    "FINAL_IMPLEMENTATION_REPORT.md",
]

# Step 1: Backup all root markdown files
print("[1/4] Backing up root markdown files...")
root_mds = list(Path(".").glob("*.md"))
for md_file in root_mds:
    if md_file.name not in KEEP_FILES:
        backup_path = backup_dir / md_file.name
        shutil.copy2(md_file, backup_path)
print(f"  [OK] Backed up {len(root_mds) - len(KEEP_FILES)} files to {backup_dir}/")
print()

# Step 2: Archive unnecessary root files
print("[2/4] Archiving unnecessary root markdown files...")
archived_count = 0
for pattern in DELETE_PATTERNS:
    file_path = Path(pattern)
    if file_path.exists():
        archive_path = archive_dir / file_path.name
        shutil.move(str(file_path), str(archive_path))
        archived_count += 1
        print(f"  - Archived: {file_path.name}")

print(f"  [OK] Archived {archived_count} files")
print()

# Step 3: Clean up old metadata files in Done folders
print("[3/4] Cleaning up old metadata files...")
metadata_count = 0

# Find all Done folders
done_folders = [
    Path("AI_Employee_Vault/Done"),
    Path("Silver_Tier_FTE/Done"),
    Path("Platinum_Tier/Done"),
    Path("Gold_Tier/Done"),
]

for done_folder in done_folders:
    if done_folder.exists():
        # Find metadata files older than 7 days
        metadata_files = list(done_folder.glob("*_metadata.md"))

        for md_file in metadata_files:
            # Archive old metadata files
            archive_path = archive_dir / "metadata" / md_file.name
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(md_file), str(archive_path))
            metadata_count += 1

print(f"  [OK] Archived {metadata_count} old metadata files")
print()

# Step 4: Clean up duplicate tier documentation
print("[4/4] Cleaning up tier-specific documentation...")
tier_docs_cleaned = 0

# Archive redundant tier documentation
tier_doc_patterns = [
    "Silver_Tier_FTE/*.md",
    "Gold_Tier/*.md",
    "Platinum_Tier/*.md",
]

redundant_tier_docs = [
    "Status_Report.md",
    "Status_Update.md",
    "Final_Status_Report.md",
    "Scan_Report.md",
    "Dashboard_Analytics.md",
    "Scheduler_Setup_Guide.md",
    "Test_Suite_Documentation.md",
    "User_Guide.md",
    "Backup_Recovery_System.md",
    "Security_Best_Practices.md",
    "FINAL_SESSION_REPORT.md",
    "Continuous_Monitoring_Report.md",
]

for tier_folder in ["Silver_Tier_FTE", "Gold_Tier", "Platinum_Tier"]:
    tier_path = Path(tier_folder)
    if tier_path.exists():
        for doc_name in redundant_tier_docs:
            doc_path = tier_path / doc_name
            if doc_path.exists():
                archive_path = archive_dir / tier_folder / doc_name
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(doc_path), str(archive_path))
                tier_docs_cleaned += 1

print(f"  [OK] Archived {tier_docs_cleaned} redundant tier documents")
print()

# Summary
print("=" * 80)
print("CLEANUP SUMMARY")
print("=" * 80)
print()
print(f"Root files archived: {archived_count}")
print(f"Metadata files archived: {metadata_count}")
print(f"Tier docs archived: {tier_docs_cleaned}")
print(f"Total files cleaned: {archived_count + metadata_count + tier_docs_cleaned}")
print()
print("Files kept in root:")
for keep_file in sorted(KEEP_FILES):
    if Path(keep_file).exists():
        print(f"  [KEEP] {keep_file}")
print()
print(f"Backup location: {backup_dir}/")
print(f"Archive location: {archive_dir}/")
print()
print("To restore files: Copy from _BACKUP_BEFORE_CLEANUP/")
print("To permanently delete: Delete _ARCHIVED_DOCS/ folder")
print()
print("=" * 80)
