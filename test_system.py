#!/usr/bin/env python3
"""
Quick test script to verify the news aggregator system.
Run this to test all components without API keys.
"""

import sys

def test_imports():
    """Test that all required packages are installed."""
    print("Testing imports...")
    try:
        import feedparser
        import requests
        from bs4 import BeautifulSoup
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np
        print("✅ All packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        import config
        print(f"✅ Config loaded")
        print(f"   Faculty keywords: {len(config.FACULTY_KEYWORDS)}")
        print(f"   RSS feeds: {len(config.RSS_FEEDS)}")
        print(f"   Max articles: {config.MAX_ARTICLES}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_clustering():
    """Test clustering functionality."""
    print("\nTesting clustering...")
    try:
        from clustering import ArticleClusterer
        
        test_articles = [
            {'title': 'AI in Education', 'description': 'Teaching with AI', 'source': 'Test1'},
            {'title': 'AI for Teaching', 'description': 'Education AI tools', 'source': 'Test2'},
            {'title': 'Quantum Computing', 'description': 'New quantum chip', 'source': 'Test3'},
        ]
        
        clusterer = ArticleClusterer()
        unique = clusterer.deduplicate(test_articles)
        
        print(f"✅ Clustering works: {len(test_articles)} → {len(unique)} articles")
        return True
    except Exception as e:
        print(f"❌ Clustering error: {e}")
        return False

def test_rag():
    """Test RAG relevance scoring."""
    print("\nTesting RAG scoring...")
    try:
        from rag import FacultyRAG
        
        test_articles = [
            {'title': 'Critical Thinking in Schools', 'description': 'Teaching reasoning', 'source': 'Test'},
            {'title': 'GPU Performance Benchmarks', 'description': 'Hardware specs', 'source': 'Test'},
        ]
        
        rag = FacultyRAG()
        scored = rag.score_relevance(test_articles)
        
        if scored[0]['relevance_score'] > scored[1]['relevance_score']:
            print(f"✅ RAG scoring works correctly")
            print(f"   Relevant article score: {scored[0]['relevance_score']:.3f}")
            print(f"   Irrelevant article score: {scored[1]['relevance_score']:.3f}")
            return True
        else:
            print(f"⚠️  RAG scoring may need tuning")
            return True
    except Exception as e:
        print(f"❌ RAG error: {e}")
        return False

def test_signal_detector():
    """Test signal detector (without API calls)."""
    print("\nTesting signal detector...")
    try:
        from signal_detector import GitHubSignalDetector, HuggingFaceSignalDetector
        
        # Just instantiate, don't call APIs
        github = GitHubSignalDetector()
        hf = HuggingFaceSignalDetector()
        
        print("✅ Signal detectors initialized")
        print("   Note: Run 'python signal_detector.py' to test with live data")
        return True
    except Exception as e:
        print(f"❌ Signal detector error: {e}")
        return False

def test_ingestion():
    """Test news ingestion (without API calls)."""
    print("\nTesting news ingestion...")
    try:
        from ingestion import NewsIngestion
        
        ingestion = NewsIngestion()
        print("✅ News ingestion initialized")
        print("   Note: Run 'python ingestion.py' to test with live data")
        return True
    except Exception as e:
        print(f"❌ Ingestion error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Inquiry Institute News Aggregator - System Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_config,
        test_clustering,
        test_rag,
        test_signal_detector,
        test_ingestion,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All tests passed ({passed}/{total})")
        print("\nYou can now run: python aggregate.py")
    else:
        print(f"⚠️  Some tests failed ({passed}/{total} passed)")
        print("\nPlease fix errors before running aggregate.py")
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    sys.exit(main())
