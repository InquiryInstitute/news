let newsData = [];

async function loadNewsData() {
    try {
        const response = await fetch('news_data.json');
        const data = await response.json();
        newsData = data.items || [];
        return newsData;
    } catch (error) {
        console.error('Error loading news data:', error);
        // Fallback data
        newsData = [
            {
                title: "AI and Critical Thinking: New Perspectives",
                source: "Tech Review",
                date: "2026-03-04",
                description: "Exploring how artificial intelligence is reshaping our approach to inquiry-based learning and critical analysis.",
                url: "#"
            },
            {
                title: "Education Reform: The Inquiry Method",
                source: "Education Weekly",
                date: "2026-03-03",
                description: "Schools worldwide are adopting inquiry-based learning methods to foster deeper student engagement.",
                url: "#"
            },
            {
                title: "Science Communication in the Digital Age",
                source: "Science Today",
                date: "2026-03-02",
                description: "How researchers are using new platforms to share findings and engage with the public.",
                url: "#"
            }
        ];
        return newsData;
    }
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function getTypeIcon(type) {
    const icons = {
        'github_trending': '🔥',
        'model_release': '🤖',
        'benchmark_update': '📊',
        'article': '📰'
    };
    return icons[type] || '📄';
}

function createNewsCard(article) {
    const icon = getTypeIcon(article.type);
    const score = article.relevance_score;
    const scoreDisplay = score ? `<span class="score" title="Relevance Score">${(score * 100).toFixed(0)}%</span>` : '';
    const keywords = article.metadata?.matched_keywords;
    const keywordsDisplay = keywords && keywords.length > 0 
        ? `<div class="keywords">${keywords.map(k => `<span class="keyword">${k}</span>`).join('')}</div>`
        : '';
    
    return `
        <article class="news-card" data-type="${article.type}">
            <div class="card-header">
                <span class="type-icon">${icon}</span>
                ${scoreDisplay}
            </div>
            <h2>${article.title}</h2>
            <div class="meta">
                <span class="source">${article.source}</span>
                <span class="date">${formatDate(article.date)}</span>
            </div>
            <p class="description">${article.description}</p>
            ${keywordsDisplay}
            <a href="${article.url}" target="_blank" rel="noopener noreferrer">Read More</a>
        </article>
    `;
}

async function renderNews() {
    const newsFeed = document.getElementById('news-feed');
    
    try {
        await loadNewsData();
        
        if (newsData.length === 0) {
            newsFeed.innerHTML = '<div class="no-data">No news available yet. Check back soon!</div>';
            return;
        }
        
        const newsHTML = newsData.map(article => createNewsCard(article)).join('');
        newsFeed.innerHTML = newsHTML;
        
        // Update last updated time
        const lastUpdated = document.getElementById('last-updated');
        if (lastUpdated) {
            lastUpdated.textContent = `Last updated: ${new Date().toLocaleString()}`;
        }
        
    } catch (error) {
        console.error('Error rendering news:', error);
        newsFeed.innerHTML = '<div class="error">Error loading news. Please try again later.</div>';
    }
}

document.addEventListener('DOMContentLoaded', renderNews);
