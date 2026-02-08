# Update Dashboard Skill

## Purpose
Summarize processed files and update the Dashboard.md with current status.

## Trigger
When metadata files appear in `/Needs_Action` directory

## Actions
1. Read metadata file content
2. Extract key information:
   - Filename
   - File type
   - Processing timestamp
   - Content summary
3. Append formatted summary to Dashboard.md
4. Move processed files to `/Done`

## Dashboard Format
```markdown
## File Processed: {filename}
Type: {file_type}
Summary of content:
{metadata_content}

Processed at: {timestamp}
```

## Integration
Works in conjunction with process_inbox skill and filesystem watcher.

## Success Criteria
- Dashboard.md updated with new entry
- Files moved to /Done folder
- Chronological order maintained
- No duplicate entries
