"""GoToSocial poster for sharing news articles."""
import requests
from typing import List, Dict, Optional
import config
import os

class GoToSocialPoster:
    """Post news articles to GoToSocial/Mastodon instance."""
    
    def __init__(self):
        self.api_token = os.getenv('GOTOSOCIAL_API_TOKEN', '')
        self.instance_url = os.getenv('GOTOSOCIAL_URL', 'https://social.inquiry.institute')
        self.enabled = bool(self.api_token)
        
        if not self.enabled:
            print("⚠️  GoToSocial posting disabled (no API token)")
        else:
            print(f"✅ GoToSocial posting enabled: {self.instance_url}")
    
    def format_post(self, article: Dict, max_length: int = 500) -> str:
        """Format article as a social media post."""
        title = article.get('title', 'Untitled')
        url = article.get('url', '')
        description = article.get('description', '')
        source = article.get('source', 'Unknown')
        score = article.get('relevance_score', 0)
        
        # Get article type icon
        article_type = article.get('type', 'article')
        icons = {
            'github_trending': '🔥',
            'model_release': '🤖',
            'benchmark_update': '📊',
            'article': '📰'
        }
        icon = icons.get(article_type, '📄')
        
        # Get faculty interests
        interested_faculty = article.get('metadata', {}).get('interested_faculty', [])
        faculty_mentions = ''
        if interested_faculty:
            # Limit to top 3 faculty
            faculty_names = [f['name'] for f in interested_faculty[:3]]
            if len(faculty_names) > 0:
                faculty_mentions = f"\n\n👥 Relevant for: {', '.join(faculty_names)}"
                if len(interested_faculty) > 3:
                    faculty_mentions += f" +{len(interested_faculty) - 3} more"
        
        # Build post
        post = f"{icon} {title}\n\n"
        
        # Add description (truncated if needed)
        desc_max = max_length - len(post) - len(url) - len(faculty_mentions) - 50
        if description and desc_max > 50:
            if len(description) > desc_max:
                description = description[:desc_max-3] + "..."
            post += f"{description}\n\n"
        
        post += f"🔗 {url}"
        post += faculty_mentions
        post += f"\n\n#InquiryInstitute #News"
        
        # Add topic hashtags
        keywords = article.get('metadata', {}).get('matched_keywords', [])
        if keywords:
            # Convert to hashtags (limit to 3, clean up)
            hashtags = ['#' + kw.replace(' ', '').replace('-', '') for kw in keywords[:3]]
            post += ' ' + ' '.join(hashtags)
        
        return post
    
    def post_status(self, status_text: str, visibility: str = 'public') -> Optional[Dict]:
        """Post a status to GoToSocial."""
        if not self.enabled:
            return None
        
        try:
            response = requests.post(
                f"{self.instance_url}/api/v1/statuses",
                headers={
                    'Authorization': f'Bearer {self.api_token}',
                    'Content-Type': 'application/json',
                },
                json={
                    'status': status_text,
                    'visibility': visibility,
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                status_url = data.get('url', '')
                print(f"✅ Posted to GoToSocial: {status_url}")
                return data
            else:
                print(f"❌ GoToSocial API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error posting to GoToSocial: {e}")
            return None
    
    def post_articles(self, articles: List[Dict], max_posts: int = 5) -> int:
        """Post top articles to GoToSocial."""
        if not self.enabled:
            print("⚠️  Skipping GoToSocial posting (disabled)")
            return 0
        
        print(f"\n📱 Posting top {max_posts} articles to GoToSocial...")
        
        posted_count = 0
        for i, article in enumerate(articles[:max_posts], 1):
            print(f"\nPost {i}/{max_posts}:")
            print(f"  Title: {article.get('title', 'Untitled')}")
            print(f"  Score: {article.get('relevance_score', 0):.3f}")
            
            # Format and post
            post_text = self.format_post(article)
            result = self.post_status(post_text)
            
            if result:
                posted_count += 1
                # Add a small delay between posts to be respectful of API
                import time
                if i < max_posts:
                    time.sleep(2)
            else:
                print(f"  ⚠️  Skipped due to error")
        
        print(f"\n✅ Posted {posted_count}/{max_posts} articles to GoToSocial")
        return posted_count

if __name__ == '__main__':
    # Test with sample article
    test_article = {
        'type': 'article',
        'title': 'New Study on Critical Thinking in AI Education',
        'description': 'Researchers at Stanford develop new framework for teaching critical thinking skills in the age of AI assistants.',
        'url': 'https://example.com/article',
        'source': 'Education Weekly',
        'relevance_score': 0.95,
        'metadata': {
            'matched_keywords': ['critical thinking', 'education', 'AI'],
            'interested_faculty': [
                {'name': 'John Dewey', 'slug': 'john-dewey'},
                {'name': 'Martha Nussbaum', 'slug': 'martha-nussbaum'}
            ]
        }
    }
    
    poster = GoToSocialPoster()
    if poster.enabled:
        post_text = poster.format_post(test_article)
        print("\n" + "="*60)
        print("TEST POST:")
        print("="*60)
        print(post_text)
        print("="*60)
        print(f"\nPost length: {len(post_text)} characters")
    else:
        print("Set GOTOSOCIAL_API_TOKEN to test posting")
