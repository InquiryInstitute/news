"""Main aggregation pipeline - orchestrates all components."""
import json
from datetime import datetime
from signal_detector import detect_all_signals
from ingestion import ingest_all_news
from clustering import ArticleClusterer
from rag import ContentSelector
from gotosocial_poster import GoToSocialPoster
import config

def run_aggregation():
    """Run the complete news aggregation pipeline."""
    print("=" * 60)
    print("🚀 Inquiry Institute News Aggregator")
    print("=" * 60)
    
    # Step 1: Detect signals
    print("\n📡 STEP 1: Detecting AI signals...")
    signals = detect_all_signals()
    print(f"   Found {len(signals)} signals")
    
    # Step 2: Ingest news
    print("\n📥 STEP 2: Ingesting news articles...")
    articles = ingest_all_news()
    print(f"   Ingested {len(articles)} articles")
    
    # Step 3: Deduplicate
    print("\n🔄 STEP 3: Deduplicating content...")
    clusterer = ArticleClusterer()
    unique_articles = clusterer.deduplicate(articles)
    print(f"   {len(unique_articles)} unique articles")
    
    # Step 4: RAG selection
    print("\n🎯 STEP 4: Selecting faculty-relevant content...")
    selector = ContentSelector()
    final_content = selector.select_content(unique_articles, signals)
    print(f"   Selected {len(final_content)} items")
    
    # Step 5: Save results
    print("\n💾 STEP 5: Saving results...")
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'total_items': len(final_content),
        'items': final_content
    }
    
    with open(config.OUTPUT_FILE, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"   Saved to {config.OUTPUT_FILE}")
    
    # Step 6: Post to GoToSocial
    print("\n📱 STEP 6: Posting to GoToSocial...")
    poster = GoToSocialPoster()
    faculty_posts = poster.post_articles(final_content, max_posts_per_faculty=3)
    total_posts = sum(faculty_posts.values())
    print(f"   Posted {total_posts} articles across {len([c for c in faculty_posts.values() if c > 0])} faculty accounts")
    
    # Step 7: Display top items
    print("\n✨ TOP 5 ITEMS:")
    print("-" * 60)
    for i, item in enumerate(final_content[:5], 1):
        score = item.get('relevance_score', 0)
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   Source: {item.get('source', 'Unknown')} | Score: {score:.3f}")
        print(f"   {item.get('url', '')}")
    
    print("\n" + "=" * 60)
    print("✅ Aggregation complete!")
    print("=" * 60)
    
    return final_content

if __name__ == '__main__':
    run_aggregation()
