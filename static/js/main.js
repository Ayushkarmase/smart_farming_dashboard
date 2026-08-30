// Main UI interactions for Smart Farming Dashboard

document.addEventListener('DOMContentLoaded', () => {
    // Mobile Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Auto-dismiss Alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => alert.remove());
        }
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Accordion functionality for FAQ page
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const item = header.parentElement;
            const isOpen = item.classList.contains('active');
            
            // Close all others
            document.querySelectorAll('.accordion-item').forEach(i => i.classList.remove('active'));
            
            if (!isOpen) {
                item.classList.add('active');
            }
        });
    });

    // Live AI News Sentiment Analyzer Tool
    const liveAnalyzeBtn = document.getElementById('btn-analyze-live');
    const liveInput = document.getElementById('live-sentiment-input');
    const liveResultCard = document.getElementById('live-sentiment-result');

    if (liveAnalyzeBtn && liveInput && liveResultCard) {
        liveAnalyzeBtn.addEventListener('click', async () => {
            const text = liveInput.value.trim();
            if (!text) {
                alert('Please enter agricultural headline or news text to analyze.');
                return;
            }

            liveAnalyzeBtn.disabled = true;
            liveAnalyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

            try {
                const response = await fetch('/news/analyze-live', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text })
                });
                const data = await response.json();

                liveResultCard.style.display = 'block';
                const badge = document.getElementById('live-badge');
                const scoreText = document.getElementById('live-score');
                const confText = document.getElementById('live-confidence');

                badge.className = 'tag';
                if (data.sentiment === 'Positive') {
                    badge.classList.add('tag-positive');
                    badge.innerHTML = '<i class="fas fa-arrow-trend-up"></i> Positive Outlook';
                } else if (data.sentiment === 'Negative') {
                    badge.classList.add('tag-negative');
                    badge.innerHTML = '<i class="fas fa-arrow-trend-down"></i> Negative / Cautionary';
                } else {
                    badge.classList.add('tag-neutral');
                    badge.innerHTML = '<i class="fas fa-minus"></i> Neutral Tone';
                }

                scoreText.textContent = `Polarity Score: ${data.score > 0 ? '+' : ''}${data.score}`;
                confText.textContent = `Model Confidence: ${data.confidence}%`;

            } catch (err) {
                console.error(err);
                alert('Failed to analyze sentiment. Please try again.');
            } finally {
                liveAnalyzeBtn.disabled = false;
                liveAnalyzeBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> Classify Sentiment';
            }
        });
    }
});
