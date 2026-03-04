# Project Summary: Inquiry Institute News Aggregator

## 🎯 Overview

An intelligent, automated news aggregation system for the Inquiry Institute that combines AI signal detection, multi-source news ingestion, semantic deduplication, and RAG-based content filtering to curate faculty-relevant content.

## 📊 System Components

### 1. **Signal Detectors** (`signal_detector.py`)
Monitors AI ecosystem for breaking developments:
- **GitHub Trending**: Repos gaining >1k stars in 24h
- **HuggingFace Models**: New model releases
- **Benchmarks**: New benchmark leaders (extensible)

### 2. **News Ingestion** (`ingestion.py`)
Multi-source content aggregation:
- RSS feeds (arXiv, Hacker News, Reddit ML, Google AI, OpenAI)
- NewsAPI integration (optional)
- Automatic date filtering (7-day window)
- HTML cleaning and normalization

### 3. **Clustering & Deduplication** (`clustering.py`)
Intelligent duplicate detection:
- TF-IDF vectorization
- Cosine similarity scoring (threshold: 0.85)
- Automatic merging of duplicate source attribution
- Topic clustering capabilities

### 4. **RAG System** (`rag.py`)
Faculty-relevance scoring:
- Semantic similarity to faculty interest profile
- Keyword matching and highlighting
- Relevance score calculation
- Signal boosting (1.5x multiplier)
- Top-N selection (50 articles)

### 5. **Orchestration** (`aggregate.py`)
Main pipeline coordinator:
- Sequential execution of all components
- JSON output generation
- Progress logging
- Error handling

## 🤖 Automation

### GitHub Actions (`.github/workflows/aggregate.yml`)
- **Frequency**: Every 6 hours
- **Manual Trigger**: Available via workflow_dispatch
- **Process**:
  1. Checkout repository
  2. Setup Python 3.11
  3. Install dependencies
  4. Run aggregation with API keys
  5. Commit updated news_data.json
  6. Push to main branch
  7. Trigger GitHub Pages rebuild

### Required Secrets
- `GH_TOKEN`: GitHub API rate limits (recommended)
- `OPENAI_API_KEY`: Enhanced embeddings (optional)
- `NEWS_API_KEY`: Additional news sources (optional)
- `HF_TOKEN`: HuggingFace access (optional)

## 🎨 Frontend

### Design Features
- Responsive grid layout (CSS Grid, auto-fill)
- Type-specific styling:
  - 🔥 GitHub trending: Orange border
  - 🤖 Model releases: Blue border
  - 📊 Benchmarks: Green border
  - 📰 Articles: Default
- Relevance score badges (gradient purple)
- Keyword tags
- Smooth hover animations
- Mobile-first responsive design

### Dynamic Loading
- Fetches from `news_data.json`
- Fallback to sample data on error
- Last updated timestamp
- Loading states and error handling

## 📈 Content Flow

```
Signal Detection → News Ingestion → Deduplication → RAG Scoring → Top 50 → JSON
      ↓                ↓                  ↓              ↓           ↓
  GitHub API      RSS Feeds        TF-IDF Cosine   Semantic      news_data.json
  HF API          NewsAPI          Similarity      Matching            ↓
  Benchmarks      arXiv                                          GitHub Pages
```

## 🔧 Configuration (`config.py`)

### Faculty Keywords (Relevance Scoring)
```python
'critical thinking', 'education', 'inquiry-based learning',
'research methodology', 'scientific method', 'media literacy',
'cognitive science', 'reasoning', 'argumentation', 'epistemology',
'pedagogy', 'assessment', 'learning sciences'
```

### RSS Sources
- Hacker News
- arXiv CS.AI & CS.LG
- Reddit r/MachineLearning
- Google AI Blog
- OpenAI Blog

### Thresholds
- GitHub stars: 1000 in 24h
- Similarity: 0.85 (duplicates)
- Max articles: 50
- Article age: 7 days

## 📦 Dependencies

**Core**:
- `feedparser`: RSS feed parsing
- `requests`: HTTP client
- `beautifulsoup4`: HTML cleaning
- `scikit-learn`: TF-IDF, clustering, similarity
- `numpy`: Numerical operations

**AI/ML**:
- `sentence-transformers`: Semantic embeddings
- `huggingface-hub`: Model tracking
- `openai`: Enhanced embeddings (optional)

**APIs**:
- `PyGithub`: GitHub API
- `python-dotenv`: Environment management

## 🚀 Deployment

### Repository
- **URL**: https://github.com/dcmcshan/inquiry-institute-news
- **Visibility**: Public
- **Default Branch**: main

### GitHub Pages
- **URL**: https://dcmcshan.github.io/inquiry-institute-news/
- **Build Type**: Legacy (automatic from main branch)
- **Source**: main branch, root path
- **HTTPS**: Enforced

### Automated Updates
1. GitHub Actions runs every 6h
2. Python aggregation executes
3. news_data.json updates
4. Commit pushed to main
5. Pages auto-rebuilds (~1-2 min)
6. Frontend loads new data

## 🎓 Faculty Customization

### Add Keywords
Edit `config.py` → `FACULTY_KEYWORDS` array

### Add Sources
Edit `config.py` → `RSS_FEEDS` array

### Adjust Scoring
Modify `rag.py` → `FacultyRAG` class

### Change Frequency
Edit `.github/workflows/aggregate.yml` → cron schedule

## 🧪 Testing

Individual component testing:
```bash
python signal_detector.py  # Test signal detection
python ingestion.py        # Test news ingestion
python clustering.py       # Test deduplication
python rag.py             # Test RAG scoring
python aggregate.py       # Full pipeline
```

## 📊 Metrics & Monitoring

View in GitHub Actions:
- Execution time
- Articles ingested
- Duplicates removed
- Signals detected
- Final article count
- Error logs

## 🔮 Future Enhancements

### Potential Additions
1. **Enhanced Benchmarks**: Scrape Papers with Code, LMSYS
2. **Social Signals**: Twitter/X trending topics
3. **Academic Tracking**: Citation counts, paper releases
4. **Advanced RAG**: Vector DB, fine-tuned embeddings
5. **User Interface**: Filters, search, categories
6. **Analytics**: View tracking, engagement metrics
7. **Email Digest**: Weekly summaries
8. **RSS Output**: Generate custom RSS feed

### Architecture Improvements
1. Database storage (SQLite/PostgreSQL)
2. Caching layer (Redis)
3. API endpoint for dynamic queries
4. Admin dashboard for configuration
5. A/B testing for relevance algorithms

## 📝 Files Structure

```
inquiry-institute-news/
├── .github/workflows/
│   └── aggregate.yml          # Automation workflow
├── .env.example              # Environment template
├── .gitignore               # Git exclusions
├── README.md                # Full documentation
├── QUICKSTART.md            # Setup guide
├── requirements.txt         # Python dependencies
├── config.py               # Configuration
├── signal_detector.py      # AI signals
├── ingestion.py           # News fetching
├── clustering.py          # Deduplication
├── rag.py                # Relevance scoring
├── aggregate.py          # Main orchestrator
├── index.html           # Frontend HTML
├── styles.css          # Frontend styling
├── app.js             # Frontend logic
└── news_data.json     # Generated content (auto-updated)
```

## ✅ Deliverables Complete

1. ✅ GitHub repository created
2. ✅ GitHub Pages enabled
3. ✅ Signal detectors implemented (GitHub, HF, benchmarks)
4. ✅ Multi-source ingestion pipeline
5. ✅ Clustering & deduplication
6. ✅ RAG-based faculty relevance filtering
7. ✅ GitHub Actions automation (6-hour cycle)
8. ✅ Modern responsive frontend
9. ✅ Comprehensive documentation
10. ✅ Sample data for immediate display

## 🌐 Live Site

**https://dcmcshan.github.io/inquiry-institute-news/**

The site is now live and will automatically update every 6 hours with fresh, faculty-relevant content!
