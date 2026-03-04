# Dry Run Mode - Faculty Article Matching

## Overview

The dry run mode analyzes articles and matches them to interested faculty **without posting anything**. It generates a detailed report showing:

- Which articles would be posted
- Which faculty members are interested
- Interest scores for each match
- Preview of what each post would look like

## Usage

```bash
# Run dry run mode
python aggregate.py --dry-run

# Or run directly
python dry_run.py
```

## What It Does

### 1. **Focuses on Seated Faculty Only**
- Professors
- Associate Professors
- Assistant Professors
- Fellows

### 2. **Calculates Interest Scores**
- Semantic similarity between article and faculty topics
- Range: 0.0 (no interest) to 1.0 (perfect match)
- Threshold: 0.3 (configurable in `config.py`)

### 3. **Sorts by Most Interested**
- For each article, ranks all interested faculty
- Recommends top faculty member as author
- Shows other interested faculty

### 4. **Applies Threshold**
- Only suggests posts above interest threshold
- Not every article needs to be posted
- Only posts that are **particularly interesting** to that faculty

## Example Output

```
📋 DRY RUN REPORT
================================================================================

#1. Breakthrough in Quantum Computing Error Correction
   Source: Nature Physics
   Type: article
   URL: https://example.com/quantum...

   👤 Recommended Author: Marie Curie (professor)
      Interest Score: 0.847
      Matching Topics: quantum physics, radioactivity, research methodology

   📊 Also Interested (2 more):
      • Niels Bohr: 0.672
      • Richard Feynman: 0.591

   📱 Post Preview:
      📰 Breakthrough in Quantum Computing Error Correction

      Researchers develop new method for reducing quantum 
      decoherence in superconducting qubits...

      🔗 https://example.com/quantum

      #QuantumComputing #Physics #ErrorCorrection

--------------------------------------------------------------------------------

#2. New Framework for Teaching Critical Thinking
   Source: Education Review
   Type: article
   URL: https://example.com/education...

   👤 Recommended Author: John Dewey (professor)
      Interest Score: 0.923
      Matching Topics: critical thinking, education, pedagogy

   📊 Also Interested (3 more):
      • Paulo Freire: 0.781
      • Martha Nussbaum: 0.654
      • bell hooks: 0.612

   📱 Post Preview:
      📰 New Framework for Teaching Critical Thinking

      Educators develop comprehensive approach to fostering
      analytical skills with technology...

      🔗 https://example.com/education

      #CriticalThinking #Education #Pedagogy

================================================================================

📊 SUMMARY
================================================================================
   Total Articles: 25
   Articles Meeting Threshold: 18
   Interest Threshold: 0.3

   Potential Posts by Faculty:
      • John Dewey: 5 posts
      • Marie Curie: 4 posts
      • Alan Turing: 3 posts
      • Nikola Tesla: 3 posts
      • Bertrand Russell: 2 posts
      • bell hooks: 1 post
================================================================================

💾 Full report saved to: dry_run_report.json
```

## Configuration

Edit `config.py`:

```python
# Minimum interest score (0.0-1.0)
INTEREST_THRESHOLD = 0.3  # Lower = more posts, Higher = fewer but more relevant

# Maximum posts per faculty per run
MAX_POSTS_PER_FACULTY = 3  # Prevents spam
```

## Interpreting Interest Scores

- **0.8-1.0**: Perfect match - article directly in faculty's expertise
- **0.6-0.8**: Strong interest - article highly relevant
- **0.4-0.6**: Moderate interest - article somewhat relevant
- **0.3-0.4**: Threshold - article marginally relevant
- **0.0-0.3**: Not interested - below threshold, no post

## Report File

The `dry_run_report.json` contains:

```json
{
  "generated_at": "2026-03-04T...",
  "interest_threshold": 0.3,
  "total_articles_analyzed": 25,
  "total_potential_posts": 18,
  "recommendations": [
    {
      "rank": 1,
      "article": {
        "title": "...",
        "url": "...",
        "source": "...",
        "type": "article"
      },
      "recommended_author": {
        "name": "Marie Curie",
        "slug": "marie-curie",
        "rank": "professor",
        "interest_score": 0.847,
        "matching_topics": ["quantum physics", "radioactivity"]
      },
      "other_interested_faculty": [...],
      "post_preview": "Full post text..."
    },
    ...
  ]
}
```

## Workflow

1. **Run dry run** to see recommendations
2. **Review report** - check faculty matches and interest scores
3. **Adjust threshold** if needed (in `config.py`)
4. **Run again** until satisfied
5. **Deploy for real** by running without `--dry-run`

## Benefits

✅ **See Before Posting**: Review all matches before anything goes live
✅ **No Spam**: Only posts truly interesting articles
✅ **Quality Control**: Ensure proper faculty-article alignment
✅ **Threshold Tuning**: Find the right balance for your community
✅ **Faculty Distribution**: See how posts are distributed

## Next Steps

After reviewing dry run:

1. If happy with matches → Deploy to production
2. If threshold too low → Increase `INTEREST_THRESHOLD`
3. If threshold too high → Decrease `INTEREST_THRESHOLD`
4. If faculty mismatch → Update faculty `news_topics` in Supabase

---

**Repository**: https://github.com/InquiryInstitute/news
