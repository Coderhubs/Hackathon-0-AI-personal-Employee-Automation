# Sentiment Analysis Skill

## Purpose
Analyze emotional tone and sentiment of incoming content to prioritize and route appropriately.

## Trigger
Automatically applied to all incoming files for enhanced metadata.

## Sentiment Categories

### Positive (Score: 0.6 to 1.0)
- Optimistic language
- Opportunities and growth
- Achievements and success
- Collaborative tone
- Constructive feedback

### Neutral (Score: -0.5 to 0.5)
- Factual information
- Status updates
- Routine communications
- Technical content
- Objective reporting

### Negative (Score: -1.0 to -0.5)
- Problems or issues
- Complaints or concerns
- Urgent matters
- Critical feedback
- Risk warnings

## Analysis Process

### Step 1: Content Extraction
- Read full file content
- Identify key phrases
- Extract emotional indicators
- Note urgency markers

### Step 2: Sentiment Scoring
Calculate sentiment score based on:
- Positive keywords: +0.1 each
- Negative keywords: -0.1 each
- Urgency markers: +0.2 to priority
- Question marks: +0.1 (engagement)
- Exclamation marks: +0.15 (emphasis)

### Step 3: Context Analysis
Consider:
- Subject matter (technical vs personal)
- Sender relationship (internal vs external)
- Historical patterns
- Industry context

### Step 4: Priority Assignment
- **HIGH:** Negative sentiment + urgency
- **MEDIUM:** Neutral or mixed sentiment
- **LOW:** Positive sentiment, no urgency

## Keyword Indicators

### Positive Keywords
- opportunity, growth, success, achievement
- excellent, great, wonderful, fantastic
- thank you, appreciate, grateful
- excited, looking forward, pleased
- collaboration, partnership, together

### Negative Keywords
- problem, issue, concern, risk
- urgent, critical, immediate, ASAP
- failed, error, broken, down
- complaint, disappointed, frustrated
- deadline, overdue, late

### Urgency Markers
- URGENT, ASAP, CRITICAL
- "by EOD", "by end of day"
- "immediately", "right away"
- "as soon as possible"
- Multiple exclamation marks

## Output Format

Add to metadata:
```yaml
sentiment_score: 0.7
sentiment_category: positive
priority: medium
urgency_level: normal
emotional_tone: optimistic
key_themes:
  - opportunity
  - collaboration
  - growth
confidence: 0.85
```

## Integration

### With Gmail Skill
- Urgent negative emails → HIGH priority
- Positive acknowledgments → MEDIUM priority
- Routine updates → LOW priority

### With LinkedIn Skill
- Controversial topics → Flag for review
- Positive trends → Encourage engagement
- Negative sentiment → Balance perspective

### With Dashboard
- Display sentiment distribution
- Track sentiment trends over time
- Alert on negative spikes

## Quality Standards
- Analysis completed in < 5 seconds
- Confidence score ≥ 0.7
- Accurate priority assignment
- Context-aware interpretation

## Examples

### Example 1: Urgent Email
**Content:** "URGENT: Production server is down. Need immediate attention!"
**Analysis:**
- Sentiment: -0.8 (negative)
- Priority: HIGH
- Urgency: critical
- Themes: technical issue, downtime

### Example 2: Positive LinkedIn
**Content:** "Excited to share our team's achievement in AI innovation!"
**Analysis:**
- Sentiment: +0.9 (positive)
- Priority: MEDIUM
- Urgency: normal
- Themes: achievement, innovation

### Example 3: Neutral Update
**Content:** "Quarterly review meeting scheduled for Tuesday at 2 PM."
**Analysis:**
- Sentiment: 0.0 (neutral)
- Priority: MEDIUM
- Urgency: normal
- Themes: meeting, routine

## Success Criteria
- Accurate sentiment detection (90%+ accuracy)
- Appropriate priority assignment
- Enhanced routing decisions
- Improved response quality
- Better resource allocation