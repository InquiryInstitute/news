"""Signal detectors for AI developments."""
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import config

class GitHubSignalDetector:
    """Detect trending GitHub repos with significant star growth."""
    
    def __init__(self):
        self.headers = {}
        if config.GITHUB_TOKEN:
            self.headers['Authorization'] = f'token {config.GITHUB_TOKEN}'
    
    def get_trending_repos(self) -> List[Dict]:
        """Get repos with >1k stars in last 24h."""
        signals = []
        
        # Search for recently created/updated AI-related repos
        topics = ['artificial-intelligence', 'machine-learning', 'deep-learning', 'llm', 'gpt']
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        for topic in topics:
            try:
                url = 'https://api.github.com/search/repositories'
                params = {
                    'q': f'topic:{topic} created:>{yesterday}',
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 10
                }
                
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for repo in data.get('items', []):
                        if repo['stargazers_count'] >= config.GITHUB_STAR_THRESHOLD:
                            signals.append({
                                'type': 'github_trending',
                                'title': f"🔥 Trending: {repo['full_name']}",
                                'description': repo['description'] or 'No description',
                                'url': repo['html_url'],
                                'stars': repo['stargazers_count'],
                                'source': 'GitHub',
                                'date': repo['created_at'],
                                'metadata': {
                                    'language': repo.get('language'),
                                    'topics': repo.get('topics', [])
                                }
                            })
            except Exception as e:
                print(f"Error fetching GitHub trends for {topic}: {e}")
        
        return signals

class HuggingFaceSignalDetector:
    """Detect new model releases and benchmark leaders."""
    
    def get_new_models(self) -> List[Dict]:
        """Get recently released models from Hugging Face."""
        signals = []
        
        try:
            url = 'https://huggingface.co/api/models'
            params = {
                'sort': 'lastModified',
                'direction': -1,
                'limit': 20,
                'filter': 'text-generation'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                models = response.json()
                for model in models[:5]:  # Top 5 recent models
                    signals.append({
                        'type': 'model_release',
                        'title': f"🤖 New Model: {model['modelId']}",
                        'description': f"Downloads: {model.get('downloads', 0):,} | Likes: {model.get('likes', 0)}",
                        'url': f"https://huggingface.co/{model['modelId']}",
                        'source': 'Hugging Face',
                        'date': model.get('lastModified', datetime.now().isoformat()),
                        'metadata': {
                            'downloads': model.get('downloads', 0),
                            'likes': model.get('likes', 0),
                            'tags': model.get('tags', [])
                        }
                    })
        except Exception as e:
            print(f"Error fetching HuggingFace models: {e}")
        
        return signals

class BenchmarkSignalDetector:
    """Detect new benchmark leaders and records."""
    
    def get_benchmark_updates(self) -> List[Dict]:
        """Get latest benchmark results."""
        signals = []
        
        # This would ideally scrape Papers with Code or similar
        # For now, we'll return a placeholder structure
        # In production, you'd implement proper scraping
        
        try:
            # Placeholder for benchmark tracking
            # You could implement web scraping here
            pass
        except Exception as e:
            print(f"Error fetching benchmarks: {e}")
        
        return signals

def detect_all_signals() -> List[Dict]:
    """Run all signal detectors and return combined results."""
    all_signals = []
    
    print("🔍 Detecting GitHub trends...")
    github_detector = GitHubSignalDetector()
    all_signals.extend(github_detector.get_trending_repos())
    
    print("🔍 Detecting new models...")
    hf_detector = HuggingFaceSignalDetector()
    all_signals.extend(hf_detector.get_new_models())
    
    print("🔍 Detecting benchmark updates...")
    benchmark_detector = BenchmarkSignalDetector()
    all_signals.extend(benchmark_detector.get_benchmark_updates())
    
    return all_signals

if __name__ == '__main__':
    signals = detect_all_signals()
    print(f"\n✅ Found {len(signals)} signals")
    for signal in signals[:3]:
        print(f"  • {signal['title']}")
