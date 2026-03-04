"""Supabase client for faculty data access."""
from typing import List, Dict, Optional
from supabase import create_client, Client
import config

class FacultyDatabase:
    """Access faculty interests and profiles from Supabase."""
    
    def __init__(self):
        self.client: Optional[Client] = None
        if config.SUPABASE_URL and config.SUPABASE_KEY:
            try:
                self.client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
                print("✅ Connected to Supabase")
            except Exception as e:
                print(f"⚠️  Supabase connection failed: {e}")
                print("   Using default faculty keywords")
    
    def get_faculty_keywords(self) -> List[str]:
        """Get all unique news topics from active faculty."""
        if not self.client:
            return config.DEFAULT_FACULTY_KEYWORDS
        
        try:
            # Query faculty table for news_topics
            response = self.client.table('faculty').select('news_topics, name').execute()
            
            if not response.data:
                print("⚠️  No faculty data found, using defaults")
                return config.DEFAULT_FACULTY_KEYWORDS
            
            # Collect all unique keywords
            all_keywords = set()
            faculty_count = 0
            
            for faculty in response.data:
                topics = faculty.get('news_topics', [])
                if topics and len(topics) > 0:
                    all_keywords.update(topics)
                    faculty_count += 1
            
            keywords_list = sorted(list(all_keywords))
            
            if not keywords_list:
                print("⚠️  No faculty news topics found, using defaults")
                return config.DEFAULT_FACULTY_KEYWORDS
            
            print(f"📚 Loaded {len(keywords_list)} keywords from {faculty_count} faculty members")
            return keywords_list
            
        except Exception as e:
            print(f"❌ Error fetching faculty keywords: {e}")
            print("   Using default faculty keywords")
            return config.DEFAULT_FACULTY_KEYWORDS
    
    def get_faculty_profiles(self) -> List[Dict]:
        """Get faculty profiles with news interests."""
        if not self.client:
            return []
        
        try:
            response = self.client.table('faculty').select(
                'id, name, slug, news_topics, short_bio'
            ).execute()
            
            # Filter to only faculty with news topics
            faculty_with_interests = [
                f for f in response.data 
                if f.get('news_topics') and len(f.get('news_topics', [])) > 0
            ]
            
            print(f"📋 Found {len(faculty_with_interests)} faculty with news interests")
            return faculty_with_interests
            
        except Exception as e:
            print(f"❌ Error fetching faculty profiles: {e}")
            return []
    
    def update_faculty_topics(self, faculty_id: str, topics: List[str]) -> bool:
        """Update news topics for a faculty member."""
        if not self.client:
            return False
        
        try:
            response = self.client.table('faculty').update({
                'news_topics': topics
            }).eq('id', faculty_id).execute()
            
            print(f"✅ Updated topics for faculty {faculty_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error updating faculty topics: {e}")
            return False

if __name__ == '__main__':
    # Test connection
    db = FacultyDatabase()
    keywords = db.get_faculty_keywords()
    print(f"\nFaculty Keywords ({len(keywords)}):")
    for kw in keywords[:20]:  # Show first 20
        print(f"  • {kw}")
    
    if len(keywords) > 20:
        print(f"  ... and {len(keywords) - 20} more")
    
    profiles = db.get_faculty_profiles()
    print(f"\nFaculty with News Interests: {len(profiles)}")
    for p in profiles[:5]:  # Show first 5
        print(f"  • {p['name']}: {len(p.get('news_topics', []))} topics")
