"""Dry run analysis for faculty-article matching."""
from typing import List, Dict, Tuple
import json
from datetime import datetime
from faculty_db import FacultyDatabase
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class FacultyArticleMatcher:
    """Match articles to faculty based on interest scores."""
    
    def __init__(self, interest_threshold: float = 0.3):
        self.db = FacultyDatabase()
        self.interest_threshold = interest_threshold
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        
    def get_seated_faculty(self) -> List[Dict]:
        """Get seated faculty members (professors, not adjuncts)."""
        if not self.db.client:
            return []
        
        try:
            # Query seated faculty: professors, associate professors, assistant professors
            response = self.db.client.table('faculty').select(
                'id, name, slug, rank, news_topics, short_bio'
            ).in_('rank', [
                'professor',
                'associate_professor', 
                'assistant_professor',
                'fellow'
            ]).execute()
            
            # Filter to those with news interests
            faculty_with_interests = [
                f for f in response.data 
                if f.get('news_topics') and len(f.get('news_topics', [])) > 0
            ]
            
            print(f"📚 Found {len(faculty_with_interests)} seated faculty with news interests")
            for f in faculty_with_interests[:10]:
                topics = f.get('news_topics', [])
                print(f"   • {f['name']} ({f['rank']}): {len(topics)} topics")
            
            return faculty_with_interests
            
        except Exception as e:
            print(f"❌ Error fetching faculty: {e}")
            return []
    
    def calculate_interest_score(self, article: Dict, faculty: Dict) -> float:
        """Calculate how interested a faculty member would be in an article."""
        # Get article text
        article_text = f"{article.get('title', '')} {article.get('description', '')}"
        
        # Get faculty interests
        faculty_topics = faculty.get('news_topics', [])
        if not faculty_topics:
            return 0.0
        
        faculty_text = ' '.join(faculty_topics)
        
        # Vectorize and calculate similarity
        try:
            texts = [article_text, faculty_text]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Boost score if article type matches faculty's field
            article_type = article.get('type', 'article')
            if article_type == 'github_trending' and any('software' in t.lower() or 'programming' in t.lower() for t in faculty_topics):
                similarity *= 1.2
            
            return float(similarity)
            
        except Exception as e:
            print(f"   Error calculating similarity: {e}")
            return 0.0
    
    def match_articles_to_faculty(self, articles: List[Dict]) -> List[Dict]:
        """Match each article to interested faculty members."""
        faculty_list = self.get_seated_faculty()
        
        if not faculty_list:
            print("⚠️  No seated faculty found")
            return []
        
        matches = []
        
        print(f"\n🔍 Analyzing {len(articles)} articles against {len(faculty_list)} faculty...")
        print(f"   Interest threshold: {self.interest_threshold}")
        
        for article in articles:
            article_title = article.get('title', 'Untitled')[:60]
            
            # Calculate interest for each faculty member
            faculty_scores = []
            for faculty in faculty_list:
                score = self.calculate_interest_score(article, faculty)
                
                if score >= self.interest_threshold:
                    faculty_scores.append({
                        'faculty_id': faculty['id'],
                        'faculty_name': faculty['name'],
                        'faculty_slug': faculty['slug'],
                        'faculty_rank': faculty['rank'],
                        'interest_score': score,
                        'topics': faculty.get('news_topics', [])
                    })
            
            # Sort by interest score
            faculty_scores.sort(key=lambda x: x['interest_score'], reverse=True)
            
            if faculty_scores:
                matches.append({
                    'article': article,
                    'interested_faculty': faculty_scores,
                    'top_faculty': faculty_scores[0] if faculty_scores else None
                })
        
        print(f"\n✅ Found {len(matches)} articles with interested faculty")
        return matches
    
    def generate_post_preview(self, article: Dict, faculty: Dict) -> str:
        """Generate what the post would look like."""
        title = article.get('title', 'Untitled')
        url = article.get('url', '')
        description = article.get('description', '')
        
        # Get article type icon
        article_type = article.get('type', 'article')
        icons = {
            'github_trending': '🔥',
            'model_release': '🤖',
            'benchmark_update': '📊',
            'article': '📰'
        }
        icon = icons.get(article_type, '📄')
        
        # Build post
        post = f"{icon} {title}\n\n"
        
        # Add description (truncated)
        if description:
            if len(description) > 200:
                description = description[:197] + "..."
            post += f"{description}\n\n"
        
        post += f"🔗 {url}\n\n"
        
        # Add hashtags
        keywords = article.get('metadata', {}).get('matched_keywords', [])
        if keywords:
            hashtags = ['#' + kw.replace(' ', '').replace('-', '').title() for kw in keywords[:3]]
            post += ' '.join(hashtags)
        
        return post
    
    def create_dry_run_report(self, matches: List[Dict], output_file: str = 'dry_run_report.json'):
        """Create a detailed dry run report."""
        report = {
            'generated_at': datetime.now().isoformat(),
            'interest_threshold': self.interest_threshold,
            'total_articles_analyzed': len(matches),
            'total_potential_posts': len(matches),
            'recommendations': []
        }
        
        print(f"\n📋 DRY RUN REPORT")
        print("=" * 80)
        
        for i, match in enumerate(matches, 1):
            article = match['article']
            top_faculty = match['top_faculty']
            all_interested = match['interested_faculty']
            
            recommendation = {
                'rank': i,
                'article': {
                    'title': article.get('title', 'Untitled'),
                    'url': article.get('url', ''),
                    'source': article.get('source', 'Unknown'),
                    'type': article.get('type', 'article'),
                    'relevance_score': article.get('relevance_score', 0)
                },
                'recommended_author': {
                    'name': top_faculty['faculty_name'],
                    'slug': top_faculty['faculty_slug'],
                    'rank': top_faculty['faculty_rank'],
                    'interest_score': top_faculty['interest_score'],
                    'matching_topics': [t for t in top_faculty['topics'] if any(
                        t.lower() in article.get('title', '').lower() or 
                        t.lower() in article.get('description', '').lower()
                        for t in [t]
                    )]
                },
                'other_interested_faculty': [
                    {
                        'name': f['faculty_name'],
                        'interest_score': f['interest_score']
                    }
                    for f in all_interested[1:5]  # Top 5 others
                ],
                'post_preview': self.generate_post_preview(article, top_faculty)
            }
            
            report['recommendations'].append(recommendation)
            
            # Print summary
            print(f"\n#{i}. {article.get('title', 'Untitled')[:70]}")
            print(f"   Source: {article.get('source', 'Unknown')}")
            print(f"   Type: {article.get('type', 'article')}")
            print(f"   URL: {article.get('url', '')[:60]}...")
            print(f"\n   👤 Recommended Author: {top_faculty['faculty_name']} ({top_faculty['faculty_rank']})")
            print(f"      Interest Score: {top_faculty['interest_score']:.3f}")
            print(f"      Matching Topics: {', '.join(recommendation['recommended_author']['matching_topics'][:3])}")
            
            if len(all_interested) > 1:
                print(f"\n   📊 Also Interested ({len(all_interested)-1} more):")
                for other in all_interested[1:3]:
                    print(f"      • {other['faculty_name']}: {other['interest_score']:.3f}")
            
            print(f"\n   📱 Post Preview:")
            preview_lines = recommendation['post_preview'].split('\n')
            for line in preview_lines[:8]:  # First 8 lines
                print(f"      {line}")
            if len(preview_lines) > 8:
                print(f"      ...")
            
            print("-" * 80)
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Full report saved to: {output_file}")
        
        # Summary statistics
        print(f"\n📊 SUMMARY")
        print("=" * 80)
        print(f"   Total Articles: {report['total_articles_analyzed']}")
        print(f"   Articles Meeting Threshold: {report['total_potential_posts']}")
        print(f"   Interest Threshold: {self.interest_threshold}")
        
        # Faculty distribution
        faculty_counts = {}
        for rec in report['recommendations']:
            author = rec['recommended_author']['name']
            faculty_counts[author] = faculty_counts.get(author, 0) + 1
        
        print(f"\n   Potential Posts by Faculty:")
        for faculty, count in sorted(faculty_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"      • {faculty}: {count} posts")
        
        print("=" * 80)
        
        return report

if __name__ == '__main__':
    # Test with sample articles
    print("🧪 Testing Faculty-Article Matching System\n")
    
    matcher = FacultyArticleMatcher(interest_threshold=0.3)
    
    # Sample articles
    sample_articles = [
        {
            'title': 'Breakthrough in Quantum Computing Error Correction',
            'description': 'Researchers develop new method for reducing quantum decoherence in superconducting qubits.',
            'url': 'https://example.com/quantum',
            'source': 'Nature Physics',
            'type': 'article',
            'relevance_score': 0.92,
            'metadata': {'matched_keywords': ['quantum computing', 'physics', 'error correction']}
        },
        {
            'title': 'New Framework for Teaching Critical Thinking in Digital Age',
            'description': 'Educators develop comprehensive approach to fostering analytical skills with technology.',
            'url': 'https://example.com/education',
            'source': 'Education Review',
            'type': 'article',
            'relevance_score': 0.88,
            'metadata': {'matched_keywords': ['critical thinking', 'education', 'pedagogy']}
        },
        {
            'title': 'Trending: AI/ethical-reasoning-framework',
            'description': 'Open-source framework for building AI systems with built-in ethical considerations.',
            'url': 'https://github.com/example/ethical-ai',
            'source': 'GitHub',
            'type': 'github_trending',
            'relevance_score': 0.95,
            'metadata': {'matched_keywords': ['AI', 'ethics', 'philosophy']}
        }
    ]
    
    matches = matcher.match_articles_to_faculty(sample_articles)
    report = matcher.create_dry_run_report(matches)
    
    print(f"\n✅ Dry run complete! Check dry_run_report.json for full details.")
