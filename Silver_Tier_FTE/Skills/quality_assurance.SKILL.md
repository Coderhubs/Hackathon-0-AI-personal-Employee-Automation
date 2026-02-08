# Quality Assurance Skill

## Purpose
Ensure all outputs meet professional standards before submission for approval.

## Trigger
Automatically applied to all drafts before saving to /Pending_Approval.

## Quality Dimensions

### 1. Content Quality (40%)
- **Accuracy:** Information is correct and verifiable
- **Completeness:** All required elements present
- **Relevance:** Content addresses the core topic
- **Value:** Provides actionable insights or information
- **Originality:** Not generic or templated

### 2. Professional Standards (30%)
- **Tone:** Appropriate for audience and context
- **Grammar:** No spelling or grammatical errors
- **Formatting:** Proper structure and readability
- **Clarity:** Easy to understand, no ambiguity
- **Conciseness:** No unnecessary verbosity

### 3. Engagement (20%)
- **Hook:** Compelling opening
- **Flow:** Logical progression of ideas
- **Call-to-Action:** Clear next steps or questions
- **Readability:** Appropriate length and structure
- **Visual Appeal:** Good use of formatting

### 4. Compliance (10%)
- **Company Rules:** Follows handbook guidelines
- **HITL:** Saved to correct folder
- **Metadata:** All required fields present
- **Status Tracking:** Proper status indicators
- **Audit Trail:** Complete documentation

## Scoring System

### Score Calculation
```
Total Score = (Content × 0.4) + (Professional × 0.3) +
              (Engagement × 0.2) + (Compliance × 0.1)
```

### Score Ranges
- **9.5-10.0:** Exceptional - Ready for approval
- **9.0-9.4:** Excellent - Minor improvements possible
- **8.0-8.9:** Good - Some revisions recommended
- **7.0-7.9:** Acceptable - Significant revisions needed
- **< 7.0:** Poor - Major rework required

### Minimum Threshold
**Drafts must score ≥ 9.0 to proceed to /Pending_Approval**

## Quality Checklist

### Before Submission
- [ ] Spell check completed
- [ ] Grammar verified
- [ ] Tone appropriate for audience
- [ ] All required elements present
- [ ] Formatting consistent
- [ ] Links/references valid
- [ ] Metadata complete
- [ ] Status indicators correct
- [ ] Compliance rules followed
- [ ] Quality score ≥ 9.0

## Common Issues & Fixes

### Issue: Generic Content
**Problem:** Draft lacks specificity or unique insights
**Fix:** Add concrete examples, data, or personal perspective

### Issue: Poor Engagement
**Problem:** No hook or call-to-action
**Fix:** Add compelling opening and engagement question

### Issue: Tone Mismatch
**Problem:** Too casual or too formal for context
**Fix:** Adjust language to match audience expectations

### Issue: Incomplete Information
**Problem:** Missing key details or context
**Fix:** Add necessary background and complete all sections

### Issue: Formatting Problems
**Problem:** Poor structure or readability
**Fix:** Use bullet points, headers, proper spacing

## Quality Review Process

### Step 1: Automated Checks
- Spell check
- Grammar check
- Word count
- Required fields present
- Compliance rules met

### Step 2: Content Analysis
- Relevance to topic
- Accuracy of information
- Completeness of response
- Value provided

### Step 3: Professional Review
- Tone appropriateness
- Clarity and conciseness
- Formatting quality
- Overall polish

### Step 4: Engagement Assessment
- Opening hook strength
- Flow and structure
- Call-to-action effectiveness
- Readability score

### Step 5: Final Scoring
- Calculate total score
- Compare to threshold
- Approve or flag for revision
- Document assessment

## Output Format

Add to draft metadata:
```yaml
quality_assessment:
  content_score: 9.5/10
  professional_score: 9.5/10
  engagement_score: 9.5/10
  compliance_score: 10.0/10
  total_score: 9.6/10
  status: approved
  reviewer: QA_Skill
  timestamp: 2026-02-08 04:25:00
  notes: "Exceptional quality, ready for approval"
```

## Integration

### With LinkedIn Skill
- Verify hashtag relevance
- Check engagement elements
- Ensure professional tone
- Validate content quality

### With Gmail Skill
- Verify all points addressed
- Check professional formatting
- Ensure appropriate tone
- Validate completeness

### With Dashboard
- Log quality scores
- Track quality trends
- Identify improvement areas
- Report quality metrics

## Success Criteria
- 100% of drafts reviewed before submission
- Average quality score ≥ 9.5/10
- < 5% revision rate
- Zero compliance violations
- Consistent quality standards

## Quality Improvement

### Continuous Learning
- Track common issues
- Identify patterns
- Update quality standards
- Refine scoring criteria
- Improve automated checks

### Feedback Loop
- Collect human feedback on approved drafts
- Analyze rejection reasons
- Adjust quality thresholds
- Update best practices
- Share learnings across skills

## Examples

### High Quality Draft (9.8/10)
```
✅ Compelling hook with emoji
✅ Clear value proposition
✅ Specific examples and data
✅ Logical flow
✅ Strong call-to-action
✅ Relevant hashtags
✅ Professional tone
✅ Perfect grammar
✅ Complete metadata
✅ Compliance verified
```

### Low Quality Draft (6.5/10)
```
❌ Generic opening
❌ Vague content
❌ No specific examples
❌ Poor structure
❌ Weak call-to-action
❌ Irrelevant hashtags
❌ Inconsistent tone
❌ Grammar errors
❌ Missing metadata
❌ Compliance issues
```

## Enforcement

**CRITICAL:** No draft proceeds to /Pending_Approval with score < 9.0

If quality score is insufficient:
1. Log the issues identified
2. Create revision plan
3. Regenerate improved version
4. Re-assess quality
5. Repeat until threshold met

## Metrics Tracking

Track over time:
- Average quality scores
- Score distribution
- Revision rates
- Common issues
- Improvement trends
- Time to quality threshold