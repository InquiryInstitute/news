"""RAG system for faculty-relevant content selection."""
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import config

class FacultyRAG:
    """Retrieval-Augmented Generation for selecting faculty-relevant content."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english'
        )
        
        # Faculty interest profile
        self.faculty_profile = ' '.join(config.FACULTY_KEYWORDS)
    
    def score_relevance(self, articles: List[Dict]) -> List[Dict]:
        """Score articles by relevance to faculty interests."""
        if not articles:
            return articles
        
        print(f"\n🎯 Scoring {len(articles)} articles for faculty relevance...")
        
        try:
            # Create corpus including faculty profile
            corpus = [self.faculty_profile]
            for article in articles:
                text = f"{article.get('title', '')} {article.get('description', '')}"
                corpus.append(text)
            
            # Vectorize
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Calculate similarity to faculty profile
            faculty_vector = tfidf_matrix[0]
            article_vectors = tfidf_matrix[1:]
            
            similarities = cosine_similarity(faculty_vector, article_vectors)[0]
            
            # Add scores to articles
            scored_articles = []
            for i, article in enumerate(articles):
                article_copy = article.copy()
                article_copy['relevance_score'] = float(similarities[i])
                scored_articles.append(article_copy)
            
            # Sort by relevance
            scored_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            print(f"✅ Top article relevance: {scored_articles[0]['relevance_score']:.3f}")
            return scored_articles
            
        except Exception as e:
            print(f"❌ Error in RAG scoring: {e}")
            return articles
    
    def filter_by_threshold(self, articles: List[Dict], threshold: float = 0.1) -> List[Dict]:
        """Filter articles below relevance threshold."""
        filtered = [a for a in articles if a.get('relevance_score', 0) >= threshold]
        print(f"📊 Filtered: {len(articles)} -> {len(filtered)} articles (threshold: {threshold})")
        return filtered
    
    def get_top_articles(self, articles: List[Dict], n: int = 20) -> List[Dict]:
        """Get top N most relevant articles."""
        return articles[:n]
    
    def enhance_with_keywords(self, articles: List[Dict]) -> List[Dict]:
        """Add matched keywords to article metadata."""
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            matched_keywords = [kw for kw in config.FACULTY_KEYWORDS if kw in text]
            
            if matched_keywords:
                article['metadata']['matched_keywords'] = matched_keywords
        
        return articles

class ContentSelector:
    """Select and rank final content for posting."""
    
    def __init__(self):
        self.rag = FacultyRAG()
    
    def select_content(self, articles: List[Dict], signals: List[Dict]) -> List[Dict]:
        """Select and rank all content."""
        # Combine articles and signals
        all_content = articles + signals
        
        # Score relevance
        scored_content = self.rag.score_relevance(all_content)
        
        # Enhance with keywords
        enhanced_content = self.rag.enhance_with_keywords(scored_content)
        
        # Get top articles
        top_content = self.rag.get_top_articles(enhanced_content, config.MAX_ARTICLES)
        
        # Ensure signals are prioritized if highly relevant
        signal_boost = []
        other_content = []
        
        for item in top_content:
            if item.get('type') in ['github_trending', 'model_release', 'benchmark_update']:
                item['relevance_score'] = item.get('relevance_score', 0) * 1.5  # Boost signals
                signal_boost.append(item)
            else:
                other_content.append(item)
        
        # Re-sort with boosted signals
        final_content = sorted(signal_boost + other_content, 
                              key=lambda x: x.get('relevance_score', 0), 
                              reverse=True)
        
        return final_content[:config.MAX_ARTICLES]

if __name__ == '__main__':
    # Test
    test_articles = [
        {'title': 'Critical Thinking in AI', 'description': 'Study on reasoning', 'source': 'Test'},
        {'title': 'Latest GPU Specs', 'description': 'Hardware news', 'source': 'Test'},
    ]
    
    rag = FacultyRAG()
    scored = rag.score_relevance(test_articles)
    for article in scored:
        print(f"{article['relevance_score']:.3f} - {article['title']}")
