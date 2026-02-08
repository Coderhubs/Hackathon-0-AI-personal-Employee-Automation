# Process Inbox Skill

## Purpose
Automatically process files that appear in the AI Employee Vault Inbox folder.

## Trigger
When new files are detected in `/Inbox` directory

## Actions
1. Read the file content
2. Generate metadata including:
   - File type
   - File size
   - Creation timestamp
   - Content summary
3. Create a metadata file in `/Needs_Action`
4. Copy original file to `/Needs_Action`

## Output Format
Metadata files should be named: `{original_filename}_metadata.md`

## Integration
This skill works with the filesystem_watcher.py script to automate file processing.

## Example Metadata
```
type: file_drop
filename: example.txt
size: 1024 bytes
content_summary: Brief description of file contents
timestamp: 2026-02-08 03:45:00
```

## Success Criteria
- Metadata file created in /Needs_Action
- Original file copied to /Needs_Action
- No data loss or corruption
