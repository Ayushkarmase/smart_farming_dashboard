// Fritz-Haber Agritech: Real-Time Live Streaming Engine

document.addEventListener('DOMContentLoaded', () => {
    initLiveClock();
    initMandiStream();
    initSensorStream();
    initWeatherControls();
    initFertilizerWeatherSync();
});

// 1. Live Header Clock & Status Pulse
function initLiveClock() {
    const clockEl = document.getElementById('live-clock');
    if (!clockEl) return;

    function updateClock() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
        clockEl.textContent = timeStr;
    }
    updateClock();
    setInterval(updateClock, 1000);
}

// 2. Real-Time APMC Mandi Prices Stream
function initMandiStream() {
    const container = document.getElementById('mandi-ticker-track');
    const updateTimeEl = document.getElementById('mandi-last-update');

    async function fetchMandiUpdates() {
        try {
            const res = await fetch('/api/live-mandi');
            if (!res.ok) return;
            const data = await res.json();

            if (updateTimeEl) {
                updateTimeEl.textContent = data.timestamp;
            }

            // Update live table rows if on dashboard
            data.commodities.forEach(item => {
                const row = document.querySelector(`[data-mandi-crop="${item.crop}"]`);
                if (row) {
                    const priceEl = row.querySelector('.mandi-price');
                    const diffEl = row.querySelector('.mandi-diff');
                    
                    if (priceEl && priceEl.textContent !== `₹${item.price.toLocaleString()}`) {
                        priceEl.textContent = `₹${item.price.toLocaleString()}`;
                        priceEl.classList.add('flash-update');
                        setTimeout(() => priceEl.classList.remove('flash-update'), 1200);
                    }

                    if (diffEl) {
                        diffEl.className = `tag ${item.trend === 'up' ? 'tag-positive' : (item.trend === 'down' ? 'tag-negative' : 'tag-neutral')}`;
                        diffEl.innerHTML = `${item.trend === 'up' ? '▲ +' : (item.trend === 'down' ? '▼ ' : '')}${item.diff} (${item.pct_change > 0 ? '+' : ''}${item.pct_change}%)`;
                    }
                }
            });

        } catch (e) {
            console.warn('Mandi stream polling error:', e);
        }
    }

    // Poll every 5 seconds for live market movements
    setInterval(fetchMandiUpdates, 5000);
}

// 3. Real-Time IoT Soil Sensor Stream
function initSensorStream() {
    const moistureVal = document.getElementById('iot-moisture-val');
    const moistureBar = document.getElementById('iot-moisture-bar');
    const moistureStatus = document.getElementById('iot-moisture-status');

    const tempVal = document.getElementById('iot-temp-val');
    const phVal = document.getElementById('iot-ph-val');
    const ecVal = document.getElementById('iot-ec-val');
    
    const nVal = document.getElementById('iot-n-val');
    const pVal = document.getElementById('iot-p-val');
    const kVal = document.getElementById('iot-k-val');

    const timestampEl = document.getElementById('iot-timestamp');

    if (!moistureVal) return;

    async function updateSensorTelemetry() {
        try {
            const res = await fetch('/api/live-sensors');
            if (!res.ok) return;
            const data = await res.json();
            const s = data.sensors;

            if (timestampEl) timestampEl.textContent = data.timestamp;

            if (moistureVal) moistureVal.textContent = `${s.moisture.value}%`;
            if (moistureBar) moistureBar.style.width = `${Math.min(100, s.moisture.value)}%`;
            if (moistureStatus) {
                moistureStatus.textContent = s.moisture.status;
                moistureStatus.className = `tag tag-${s.moisture.level}`;
            }

            if (tempVal) tempVal.textContent = `${s.soil_temp.value}°C`;
            if (phVal) phVal.textContent = s.ph.value;
            if (ecVal) ecVal.textContent = `${s.ec.value} dS/m`;

            if (nVal) nVal.textContent = `${s.npk.n} mg/kg`;
            if (pVal) pVal.textContent = `${s.npk.p} mg/kg`;
            if (kVal) kVal.textContent = `${s.npk.k} mg/kg`;

        } catch (e) {
            console.warn('Sensor stream polling error:', e);
        }
    }

    // Poll every 3 seconds for continuous telemetry updates
    setInterval(updateSensorTelemetry, 3000);
}

// 4. Live Weather & City Switcher
function initWeatherControls() {
    const citySelector = document.getElementById('weather-city-select');
    const gpsBtn = document.getElementById('btn-gps-weather');

    if (citySelector) {
        citySelector.addEventListener('change', () => {
            fetchWeatherForCity(citySelector.value);
        });
    }

    if (gpsBtn) {
        gpsBtn.addEventListener('click', () => {
            if (navigator.geolocation) {
                gpsBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Locating...';
                navigator.geolocation.getCurrentPosition(
                    pos => {
                        fetchWeatherCoords(pos.coords.latitude, pos.coords.longitude);
                        gpsBtn.innerHTML = '<i class="fas fa-location-crosshairs"></i> GPS Synced';
                    },
                    err => {
                        console.warn(err);
                        alert('Location access denied. Using default regional weather.');
                        gpsBtn.innerHTML = '<i class="fas fa-location-crosshairs"></i> Locate Me';
                    }
                );
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        });
    }
}

async function fetchWeatherForCity(city) {
    try {
        const res = await fetch(`/api/live-weather?city=${encodeURIComponent(city)}`);
        const data = await res.json();
        updateWeatherUI(data);
    } catch (e) {
        console.error('Failed to load weather:', e);
    }
}

async function fetchWeatherCoords(lat, lon) {
    try {
        const res = await fetch(`/api/live-weather?lat=${lat}&lon=${lon}&city=My GPS Field`);
        const data = await res.json();
        updateWeatherUI(data);
    } catch (e) {
        console.error('Failed to load GPS weather:', e);
    }
}

function updateWeatherUI(w) {
    const tempEl = document.getElementById('weather-temp');
    const condEl = document.getElementById('weather-condition');
    const cityEl = document.getElementById('weather-city-name');
    const humEl = document.getElementById('weather-humidity');
    const windEl = document.getElementById('weather-wind');
    const rainEl = document.getElementById('weather-rain');
    const iconEl = document.getElementById('weather-icon');

    if (tempEl) tempEl.textContent = `${w.temperature}°C`;
    if (condEl) condEl.textContent = w.condition;
    if (cityEl) cityEl.textContent = w.city;
    if (humEl) humEl.textContent = `${w.humidity}%`;
    if (windEl) windEl.textContent = `${w.wind_speed} km/h`;
    if (rainEl) rainEl.textContent = `${w.precipitation} mm`;

    if (iconEl) {
        iconEl.className = `fas ${w.icon}`;
    }
}

// 5. Fertilizer Form Weather Auto-Sync
function initFertilizerWeatherSync() {
    const syncBtn = document.getElementById('btn-sync-weather-form');
    const citySelect = document.getElementById('sync-city-select');

    if (!syncBtn) return;

    syncBtn.addEventListener('click', async () => {
        const city = citySelect ? citySelect.value : 'Ratnagiri';
        syncBtn.disabled = true;
        syncBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Fetching Live Telemetry...';

        try {
            const res = await fetch(`/api/live-weather?city=${encodeURIComponent(city)}`);
            const data = await res.json();

            const tempInput = document.getElementById('temperature');
            const humInput = document.getElementById('humidity');
            const rainInput = document.getElementById('rainfall');

            if (tempInput) tempInput.value = data.temperature;
            if (humInput) humInput.value = data.humidity;
            if (rainInput) rainInput.value = Math.max(10, Math.round(data.precipitation * 30 + 110)); // Est. seasonal index

            showLiveToast(`Live climate telemetry for ${data.city} synced: ${data.temperature}°C, ${data.humidity}% Humidity.`, 'success');

        } catch (e) {
            console.error(e);
            alert('Failed to sync live weather.');
        } finally {
            syncBtn.disabled = false;
            syncBtn.innerHTML = '<i class="fas fa-cloud-bolt"></i> Auto-Fill from Live Telemetry';
        }
    });
}

// Live Toast Notification Alert
function showLiveToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `live-toast live-toast-${type}`;
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <i class="fas fa-${type === 'success' ? 'circle-check' : 'circle-info'}"></i>
            <span>${message}</span>
        </div>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; color: inherit; cursor: pointer;">&times;</button>
    `;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}
