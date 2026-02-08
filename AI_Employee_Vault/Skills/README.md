# AI Employee Agent Skills

This directory contains Agent Skills for the Bronze Tier AI Employee system.

## Available Skills

### 1. Process Inbox (`process_inbox.SKILL.md`)
Handles incoming files in the /Inbox folder, creates metadata, and moves files to /Needs_Action.

### 2. Update Dashboard (`update_dashboard.SKILL.md`)
Processes metadata files, updates Dashboard.md with summaries, and moves completed files to /Done.

### 3. Summarize Content (`summarize_content.SKILL.md`)
Analyzes file contents and generates concise summaries for the dashboard.

## Skill Architecture

```
┌─────────┐
│  Inbox  │
└────┬────┘
     │ (process_inbox skill)
     ▼
┌──────────────┐
│ Needs_Action │
└──────┬───────┘
       │ (update_dashboard + summarize_content skills)
       ▼
┌──────────┐
│   Done   │
└──────────┘
```

## Integration with Filesystem Watcher

The `filesystem_watcher.py` script monitors directories and triggers these skills:
- Watches /Inbox → triggers process_inbox
- Watches /Needs_Action → triggers update_dashboard

## Usage

These skills are designed to work autonomously with the filesystem watcher. Claude Code can also invoke these skills manually when needed.

## Bronze Tier Compliance

All AI functionality in this system is implemented as Agent Skills per Bronze Tier requirements:
- ✅ File processing automation
- ✅ Dashboard updates
- ✅ Content summarization
- ✅ Metadata generation

## Future Enhancements (Silver/Gold Tier)

- Email processing skills
- Calendar integration skills
- Task prioritization skills
- Multi-source aggregation skills
