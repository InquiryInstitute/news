# Supabase Integration Complete! 🎉

## ✅ What Was Added

### 1. **Supabase Database Connection**
- New `faculty_db.py` module for accessing faculty data
- Pulls `news_topics` field from Supabase `faculty` table
- Automatic fallback to default keywords if Supabase unavailable

### 2. **Dynamic Faculty Interests**
- System now reads faculty interests from live database
- Faculty members can update their topics in Supabase:
  ```sql
  UPDATE faculty 
  SET news_topics = ARRAY['AI', 'philosophy', 'quantum computing']
  WHERE id = 'faculty_id';
  ```

### 3. **Enhanced RAG Scoring**
- Articles scored against actual faculty interests
- Tracks which faculty members are interested in each article
- Adds `interested_faculty` metadata to articles:
  ```json
  {
    "interested_faculty": [
      {"name": "Socrates", "slug": "socrates"},
      {"name": "Plato", "slug": "plato"}
    ]
  }
  ```

### 4. **GitHub Actions Integration**
- Added `SUPABASE_URL` and `SUPABASE_KEY` secrets to repository
- Workflow now pulls live faculty data every 6 hours
- Automated, dynamic content curation

## 📊 Data Flow

```
Faculty Update Topics in Supabase
           ↓
GitHub Actions runs (every 6h)
           ↓
faculty_db.py queries Supabase
           ↓
Aggregates all unique topics
           ↓
RAG scores articles against topics
           ↓
Tracks interested faculty per article
           ↓
Saves to news_data.json
           ↓
GitHub Pages deploys
           ↓
Frontend displays with faculty tags
```

## 🔑 Configuration

### Environment Variables
```bash
# Required
SUPABASE_URL=https://pilmscrodlitdrygabvo.supabase.co
SUPABASE_KEY=eyJhbGci... (anon key)

# Optional
GITHUB_TOKEN=
OPENAI_API_KEY=
NEWS_API_KEY=
HF_TOKEN=
```

### GitHub Secrets (Already Added)
- ✅ `SUPABASE_URL`
- ✅ `SUPABASE_KEY`

## 📝 Faculty Table Schema

The system reads from the `faculty` table:

```sql
CREATE TABLE faculty (
  id text PRIMARY KEY,
  name text NOT NULL,
  slug text UNIQUE NOT NULL,
  news_topics text[],  -- Array of interest keywords
  ...
);

-- Example data
UPDATE faculty SET news_topics = ARRAY[
  'critical thinking',
  'epistemology',
  'AI ethics',
  'philosophy of mind'
] WHERE id = 'socrates';
```

## 🎯 Example Output

Articles now include faculty relevance:

```json
{
  "title": "New Study on Critical Thinking in AI",
  "relevance_score": 0.95,
  "metadata": {
    "matched_keywords": ["critical thinking", "AI", "reasoning"],
    "interested_faculty": [
      {"name": "Socrates", "slug": "socrates"},
      {"name": "John Dewey", "slug": "john-dewey"},
      {"name": "Martha Nussbaum", "slug": "martha-nussbaum"}
    ]
  }
}
```

## 🧪 Testing

```bash
# Test faculty database connection
python faculty_db.py

# Test full pipeline
python aggregate.py

# Test system
python test_system.py
```

## 🚀 Next Steps

### For Faculty Members
1. Log into Inquiry Institute platform
2. Update your `news_topics` in your profile
3. System will automatically include your interests in next aggregation

### For Administrators
1. Monitor GitHub Actions runs
2. Review faculty interests in Supabase dashboard
3. Adjust `DEFAULT_FACULTY_KEYWORDS` in `config.py` for fallback

## 🎨 Frontend Integration (Future)

The frontend can now show:
- Faculty member tags on relevant articles
- Filter by faculty member
- Faculty-specific RSS feeds
- Personalized news pages per faculty

Example enhancement:
```javascript
// Show interested faculty
if (article.metadata.interested_faculty) {
  const faculty = article.metadata.interested_faculty;
  html += `<div class="faculty-tags">`;
  faculty.forEach(f => {
    html += `<a href="/faculty/${f.slug}">${f.name}</a>`;
  });
  html += `</div>`;
}
```

## 📈 Benefits

1. **Dynamic**: No code changes needed to update interests
2. **Personalized**: Each faculty member controls their topics
3. **Scalable**: Grows with faculty additions
4. **Transparent**: Faculty can see why articles match
5. **Collaborative**: Multiple faculty can share interests

## 🔐 Security

- Uses Supabase anon key (read-only for public data)
- No sensitive faculty data exposed
- RLS policies can be added for privacy

---

**Status**: ✅ Fully Integrated and Deployed
**Repository**: https://github.com/InquiryInstitute/news
**Live Site**: https://inquiryinstitute.github.io/news/
