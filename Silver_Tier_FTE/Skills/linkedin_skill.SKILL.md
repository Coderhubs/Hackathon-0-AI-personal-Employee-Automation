# LinkedIn Skill

## Purpose
Draft professional LinkedIn posts for AI/Tech content that appears in the system.

## Trigger
When a file mentions "AI", "Tech", "Machine Learning", "Blockchain", "Cloud", "Cybersecurity", or other technology keywords.

## Actions
1. Read and analyze the content
2. Identify key themes and insights
3. Draft a professional LinkedIn post that:
   - Opens with an engaging hook (emoji optional)
   - Presents the main idea clearly
   - Includes 3-5 key implications or takeaways
   - Ends with a call-to-action question
   - Uses 5-7 relevant hashtags
4. Save draft to `/Pending_Approval` as `DRAFT_Post_[Topic].md`
5. **NEVER** post directly - always require human approval

## Output Format
```markdown
## Draft LinkedIn Post: [Title]

[Engaging opening with emoji]

[Main content with clear value proposition]

**Key points:**
• [Point 1]
• [Point 2]
• [Point 3]

[Thought-provoking question for engagement]

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5

---
**Status:** PENDING APPROVAL
**Created:** [timestamp]
**Source:** [source file]
**Sentiment:** [sentiment analysis]
**Priority:** [priority level]
```

## Quality Standards
- Professional tone appropriate for business audience
- Balanced perspective (avoid hype or fear-mongering)
- Actionable insights or thought-provoking questions
- Proper grammar and formatting
- Relevant hashtags for discoverability
- Length: 150-300 words optimal

## Integration
Works with:
- linkedin_watcher.py (monitors trends)
- Company Handbook HITL rule (requires approval)
- Dashboard logging (tracks all drafts)

## Success Criteria
- Draft created within 30 seconds
- Quality score: 9.0/10 or higher
- Saved to /Pending_Approval (not /Done)
- Human approval required before posting
- No duplicate posts on same topic

## Examples

**Good:**
- Balanced perspective on AI adoption
- Specific insights with actionable takeaways
- Engaging question that invites discussion
- Professional tone with personality

**Avoid:**
- Clickbait or sensationalism
- Generic platitudes without substance
- Overly technical jargon
- Controversial political statements
- Self-promotion without value