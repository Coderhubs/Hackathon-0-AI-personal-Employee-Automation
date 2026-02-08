# Smart Routing Skill

## Purpose
Intelligently route incoming files to appropriate processing workflows based on content analysis.

## Trigger
Applied to all files entering /Needs_Action for classification and routing.

## Routing Categories

### 1. LinkedIn Content
**Triggers:**
- Keywords: AI, Tech, Machine Learning, Innovation, Digital Transformation
- File prefix: LINKEDIN_
- Tech-related headlines
- Industry trends

**Route To:** LinkedIn Skill → Draft Post → /Pending_Approval

### 2. Gmail Messages
**Triggers:**
- File prefix: GMAIL_
- Email structure (Subject, From, To, Date)
- Meeting invitations
- Action requests

**Route To:** Gmail Skill → Draft Response → /Pending_Approval

### 3. Urgent Items
**Triggers:**
- Keywords: URGENT, CRITICAL, ASAP, IMMEDIATE
- Negative sentiment + high priority
- Deadline mentions
- Security alerts

**Route To:** High Priority Queue → Immediate Processing → Notify Human

### 4. Routine Updates
**Triggers:**
- Status reports
- Scheduled updates
- Routine communications
- Low priority items

**Route To:** Standard Processing → Low Priority Queue

### 5. Test/Verification Files
**Triggers:**
- Filename contains "test"
- Small file size (< 100 bytes)
- Verification content
- Development files

**Route To:** Test Processing → Quick Validation → /Done

## Routing Logic

### Step 1: File Analysis
```python
def analyze_file(file_path):
    # Read content
    content = read_file(file_path)

    # Extract metadata
    filename = get_filename(file_path)
    size = get_file_size(file_path)

    # Analyze content
    keywords = extract_keywords(content)
    sentiment = analyze_sentiment(content)
    urgency = detect_urgency(content)

    return {
        'filename': filename,
        'size': size,
        'keywords': keywords,
        'sentiment': sentiment,
        'urgency': urgency
    }
```

### Step 2: Classification
```python
def classify_file(analysis):
    # Check for explicit prefixes
    if 'GMAIL_' in analysis['filename']:
        return 'gmail'
    if 'LINKEDIN_' in analysis['filename']:
        return 'linkedin'

    # Check for urgency
    if analysis['urgency'] == 'critical':
        return 'urgent'

    # Check for tech keywords
    tech_keywords = ['AI', 'Tech', 'ML', 'Cloud', 'Cyber']
    if any(kw in analysis['keywords'] for kw in tech_keywords):
        return 'linkedin'

    # Check for test files
    if 'test' in analysis['filename'].lower():
        return 'test'

    # Default to routine
    return 'routine'
```

### Step 3: Route Assignment
```python
def route_file(classification, analysis):
    routes = {
        'gmail': {
            'skill': 'Gmail Skill',
            'priority': 'medium',
            'destination': '/Pending_Approval',
            'processing_time': 30
        },
        'linkedin': {
            'skill': 'LinkedIn Skill',
            'priority': 'medium',
            'destination': '/Pending_Approval',
            'processing_time': 30
        },
        'urgent': {
            'skill': 'Priority Handler',
            'priority': 'high',
            'destination': '/Pending_Approval',
            'processing_time': 15,
            'notify': True
        },
        'test': {
            'skill': 'Test Processor',
            'priority': 'low',
            'destination': '/Done',
            'processing_time': 10
        },
        'routine': {
            'skill': 'Standard Processor',
            'priority': 'low',
            'destination': '/Done',
            'processing_time': 20
        }
    }

    return routes[classification]
```

## Priority Matrix

### High Priority (Process Immediately)
- Urgent keywords present
- Negative sentiment + deadline
- Security-related content
- Executive communications
- Critical system alerts

### Medium Priority (Process Within 1 Hour)
- LinkedIn content
- Gmail responses
- Standard business communications
- Scheduled updates
- Routine requests

### Low Priority (Process Within 4 Hours)
- Test files
- Verification items
- Informational content
- Non-urgent updates
- Background tasks

## Routing Rules

### Rule 1: Explicit Prefix Override
If filename has GMAIL_ or LINKEDIN_ prefix, route directly to respective skill regardless of content.

### Rule 2: Urgency Takes Precedence
If urgency detected, escalate to high priority regardless of other factors.

### Rule 3: Sentiment-Based Routing
- Negative sentiment + urgency → High priority
- Positive sentiment → Standard priority
- Neutral sentiment → Content-based routing

### Rule 4: Size-Based Handling
- Files < 50 bytes → Quick processing
- Files 50-500 bytes → Standard processing
- Files > 500 bytes → Detailed analysis

### Rule 5: Historical Pattern Learning
Track routing decisions and outcomes to improve future routing accuracy.

## Output Format

Create routing metadata:
```yaml
routing_decision:
  classification: linkedin
  assigned_skill: LinkedIn Skill
  priority: medium
  destination: /Pending_Approval
  estimated_time: 30 seconds
  confidence: 0.95
  reasoning: "Tech keywords detected, LinkedIn prefix present"
  timestamp: 2026-02-08 04:25:00
```

## Integration

### With All Skills
- Provides initial classification
- Assigns appropriate skill
- Sets priority level
- Estimates processing time

### With Dashboard
- Logs routing decisions
- Tracks routing accuracy
- Reports classification distribution
- Monitors processing times

### With Quality Assurance
- Validates routing decisions
- Checks for misclassifications
- Suggests routing improvements
- Tracks routing quality

## Success Criteria
- Routing accuracy ≥ 95%
- Classification time < 5 seconds
- Appropriate priority assignment
- Correct skill selection
- Efficient processing flow

## Error Handling

### Misclassification Detected
1. Log the error
2. Analyze root cause
3. Update routing rules
4. Reclassify and reroute
5. Learn from mistake

### Ambiguous Content
1. Apply multiple classifications
2. Use highest priority route
3. Flag for human review
4. Document ambiguity
5. Improve classification logic

## Metrics Tracking

Track over time:
- Classification accuracy
- Routing efficiency
- Processing time by route
- Priority distribution
- Misclassification rate
- Improvement trends

## Examples

### Example 1: LinkedIn Tech Post
**Input:** "AI breakthrough in natural language processing"
**Classification:** linkedin
**Priority:** medium
**Skill:** LinkedIn Skill
**Confidence:** 0.98

### Example 2: Urgent Email
**Input:** "URGENT: Server down, need immediate attention"
**Classification:** urgent
**Priority:** high
**Skill:** Gmail Skill + Priority Handler
**Confidence:** 1.0

### Example 3: Test File
**Input:** "test_verification.txt" (50 bytes)
**Classification:** test
**Priority:** low
**Skill:** Test Processor
**Confidence:** 0.99

## Continuous Improvement

### Learning Loop
1. Track routing decisions
2. Collect outcome data
3. Analyze accuracy
4. Identify patterns
5. Update routing rules
6. Test improvements
7. Deploy updates

### Feedback Integration
- Human corrections → Update rules
- Misclassifications → Refine logic
- New patterns → Add classifications
- Performance data → Optimize routing