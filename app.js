const newsData = [
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
    },
    {
        title: "Critical Thinking Skills in the Workplace",
        source: "Business Insights",
        date: "2026-03-01",
        description: "Companies are prioritizing critical thinking and problem-solving abilities in their hiring practices.",
        url: "#"
    },
    {
        title: "Media Literacy: A Growing Necessity",
        source: "Digital Times",
        date: "2026-02-28",
        description: "Understanding how to evaluate sources and identify misinformation has never been more important.",
        url: "#"
    },
    {
        title: "Research Methods Revolution",
        source: "Academic Journal",
        date: "2026-02-27",
        description: "New methodologies are changing how researchers approach complex questions across disciplines.",
        url: "#"
    }
];

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

function createNewsCard(article) {
    return `
        <article class="news-card">
            <h2>${article.title}</h2>
            <div class="meta">
                <span class="source">${article.source}</span>
                <span class="date">${formatDate(article.date)}</span>
            </div>
            <p class="description">${article.description}</p>
            <a href="${article.url}" target="_blank" rel="noopener noreferrer">Read More</a>
        </article>
    `;
}

function renderNews() {
    const newsFeed = document.getElementById('news-feed');
    
    setTimeout(() => {
        const newsHTML = newsData.map(article => createNewsCard(article)).join('');
        newsFeed.innerHTML = newsHTML;
    }, 500);
}

document.addEventListener('DOMContentLoaded', renderNews);
