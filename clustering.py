"""Clustering and deduplication of news articles."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import config

class ArticleClusterer:
    """Detect and remove duplicate articles using semantic similarity."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on content similarity."""
        if len(articles) < 2:
            return articles
        
        print(f"\n🔄 Clustering {len(articles)} articles...")
        
        # Create text corpus
        corpus = []
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}"
            corpus.append(text)
        
        # Vectorize
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Calculate similarity matrix
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Find duplicates
            seen_indices = set()
            unique_articles = []
            
            for i in range(len(articles)):
                if i in seen_indices:
                    continue
                
                # Mark this article as seen
                seen_indices.add(i)
                
                # Find similar articles
                similar_indices = np.where(similarity_matrix[i] > config.SIMILARITY_THRESHOLD)[0]
                
                # Merge metadata from duplicates
                merged_sources = {articles[i].get('source', 'Unknown')}
                
                for j in similar_indices:
                    if j != i and j not in seen_indices:
                        seen_indices.add(j)
                        merged_sources.add(articles[j].get('source', 'Unknown'))
                
                # Add unique article with merged info
                article = articles[i].copy()
                if len(merged_sources) > 1:
                    article['source'] = f"{article['source']} +{len(merged_sources)-1} more"
                    article['metadata']['duplicate_count'] = len(similar_indices) - 1
                
                unique_articles.append(article)
            
            print(f"✅ Reduced to {len(unique_articles)} unique articles (removed {len(articles) - len(unique_articles)} duplicates)")
            return unique_articles
            
        except Exception as e:
            print(f"❌ Error in clustering: {e}")
            return articles
    
    def cluster_by_topic(self, articles: List[Dict], n_clusters: int = 5) -> Dict[str, List[Dict]]:
        """Group articles by topic."""
        from sklearn.cluster import KMeans
        
        if len(articles) < n_clusters:
            return {'all': articles}
        
        try:
            corpus = [f"{a.get('title', '')} {a.get('description', '')}" for a in articles]
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Cluster
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(tfidf_matrix)
            
            # Group by cluster
            clustered = {}
            for i, cluster_id in enumerate(clusters):
                topic = f"topic_{cluster_id}"
                if topic not in clustered:
                    clustered[topic] = []
                clustered[topic].append(articles[i])
            
            return clustered
            
        except Exception as e:
            print(f"❌ Error in topic clustering: {e}")
            return {'all': articles}

if __name__ == '__main__':
    # Test with sample data
    test_articles = [
        {'title': 'GPT-4 Released', 'description': 'OpenAI releases GPT-4', 'source': 'OpenAI'},
        {'title': 'GPT-4 Launch', 'description': 'OpenAI launches GPT-4 model', 'source': 'TechNews'},
        {'title': 'New Study on Education', 'description': 'Research shows benefits', 'source': 'EduNews'},
    ]
    
    clusterer = ArticleClusterer()
    unique = clusterer.deduplicate(test_articles)
    print(f"Test: {len(test_articles)} -> {len(unique)} articles")
