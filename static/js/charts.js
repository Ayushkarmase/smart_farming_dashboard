// Chart.js integrations for Smart Farming Dashboard

function initForecastChart(canvasId, forecastData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx || !forecastData) return;

    const allLabels = [...forecastData.historical_labels, ...forecastData.forecast_labels];
    const histLen = forecastData.historical_labels.length;
    const foreLen = forecastData.forecast_labels.length;

    // Past data filled with nulls for future
    const pastSeries = [...forecastData.historical_values, ...Array(foreLen).fill(null)];
    
    // Future data prefixed with last past data point for seamless line continuity
    const lastHistVal = forecastData.historical_values[histLen - 1];
    const futureSeries = [...Array(histLen - 1).fill(null), lastHistVal, ...forecastData.forecast_values];
    const upperSeries = [...Array(histLen - 1).fill(null), lastHistVal, ...forecastData.upper_bounds];
    const lowerSeries = [...Array(histLen - 1).fill(null), lastHistVal, ...forecastData.lower_bounds];

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: allLabels,
            datasets: [
                {
                    label: 'Historical Actual Demand (MT)',
                    data: pastSeries,
                    borderColor: '#0284c7',
                    backgroundColor: 'rgba(2, 132, 199, 0.1)',
                    borderWidth: 3,
                    pointBackgroundColor: '#0284c7',
                    pointRadius: 5,
                    tension: 0.3
                },
                {
                    label: 'AI Forecasted Demand (MT)',
                    data: futureSeries,
                    borderColor: '#10b981',
                    borderDash: [5, 5],
                    backgroundColor: 'rgba(16, 185, 129, 0.15)',
                    borderWidth: 3,
                    pointBackgroundColor: '#10b981',
                    pointRadius: 6,
                    tension: 0.3,
                    fill: false
                },
                {
                    label: 'Upper Confidence (95%)',
                    data: upperSeries,
                    borderColor: 'rgba(16, 185, 129, 0.25)',
                    borderWidth: 1,
                    pointRadius: 0,
                    fill: '+1',
                    backgroundColor: 'rgba(16, 185, 129, 0.08)',
                    tension: 0.3
                },
                {
                    label: 'Lower Confidence (95%)',
                    data: lowerSeries,
                    borderColor: 'rgba(16, 185, 129, 0.25)',
                    borderWidth: 1,
                    pointRadius: 0,
                    fill: false,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: { font: { family: 'Plus Jakarta Sans', size: 12, weight: '600' } }
                },
                tooltip: {
                    padding: 12,
                    boxPadding: 6,
                    usePointStyle: true
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: { display: true, text: 'Quantity (Metric Tonnes)', font: { weight: '600' } },
                    grid: { color: '#f1f5f9' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}
