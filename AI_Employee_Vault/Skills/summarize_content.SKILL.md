# Summarize Content Skill

## Purpose
Analyze and summarize file contents for the AI Employee system.

## Trigger
When processing files that require content analysis

## Actions
1. Read file content (text, code, documents)
2. Identify file type and purpose
3. Extract key information:
   - Main topics or themes
   - Action items (if any)
   - Important dates or deadlines
   - Key entities (people, projects, etc.)
4. Generate concise summary (2-3 sentences)

## Supported File Types
- Text files (.txt, .md)
- Code files (.py, .js, .java, etc.)
- Documents (.doc, .pdf - if readable)
- Configuration files (.json, .yaml, .xml)

## Summary Guidelines
- Keep summaries under 200 words
- Focus on actionable information
- Highlight urgency or priority
- Use clear, professional language

## Output Format
```
File Type: {type}
Summary: {concise_summary}
Action Required: {yes/no}
Priority: {low/medium/high}
```

## Integration
Used by process_inbox and update_dashboard skills.

## Success Criteria
- Accurate content identification
- Relevant information extracted
- Clear, actionable summaries
- Appropriate priority assignment
