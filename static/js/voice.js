/**
 * voice.js — Voice-to-text + AI cafe recommendation
 * Uses the Web Speech API (no install needed, browser built-in)
 */

(function () {
  const micBtn        = document.getElementById('micBtn');
  const micLabel      = document.getElementById('micLabel');
  const transcriptText = document.getElementById('transcriptText');
  const voiceStatus   = document.getElementById('voiceStatus');
  const resultsSection = document.getElementById('resultsSection');
  const resultsGrid   = document.getElementById('resultsGrid');
  const resultsQuery  = document.getElementById('resultsQuery');

  // ── Check browser support ──────────────────────────────
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    micLabel.textContent = 'Not supported in this browser';
    micBtn.disabled = true;
    voiceStatus.textContent = 'Please use Chrome or Edge for voice input.';
    return;
  }

  // ── Setup recognition ──────────────────────────────────
  const recognition = new SpeechRecognition();
  recognition.lang = 'en-PH';       // Philippine English
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;
  recognition.continuous = false;

  let isListening = false;
  let finalTranscript = '';
  let autoSubmitTimer = null;

  // ── Mic button click ───────────────────────────────────
  micBtn.addEventListener('click', () => {
    if (isListening) {
      recognition.stop();
      return;
    }
    finalTranscript = '';
    transcriptText.textContent = '';
    transcriptText.classList.remove('transcript-placeholder');
    recognition.start();
  });

  // ── Recognition events ─────────────────────────────────
  recognition.onstart = () => {
    isListening = true;
    micBtn.classList.add('listening');
    micLabel.textContent = 'Listening…';
    voiceStatus.textContent = '🎙 Speak now — describe your ideal cafe';
    resultsSection.style.display = 'none';
  };

  recognition.onresult = (event) => {
    let interim = '';
    finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const text = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += text;
      } else {
        interim += text;
      }
    }

    transcriptText.textContent = finalTranscript || interim;

    // Auto-submit 1.5 seconds after the user stops talking
    if (finalTranscript) {
      clearTimeout(autoSubmitTimer);
      autoSubmitTimer = setTimeout(() => {
        recognition.stop();
      }, 1500);
    }
  };

  recognition.onerror = (event) => {
    isListening = false;
    micBtn.classList.remove('listening');
    micLabel.textContent = 'Tap to speak';

    if (event.error === 'no-speech') {
      voiceStatus.textContent = "We didn't catch anything. Try again!";
    } else if (event.error === 'not-allowed') {
      voiceStatus.textContent = '⚠️ Microphone access denied. Please allow it in browser settings.';
    } else {
      voiceStatus.textContent = `Error: ${event.error}`;
    }
  };

  recognition.onend = () => {
    isListening = false;
    micBtn.classList.remove('listening');
    micLabel.textContent = 'Tap to speak';

    const query = finalTranscript.trim();
    if (query.length > 2) {
      voiceStatus.textContent = '✨ Got it! Finding your perfect cafe…';
      fetchRecommendations(query);
    } else {
      voiceStatus.textContent = query ? 'Say a bit more and try again.' : '';
    }
  };

  // ── Fetch recommendations from server ─────────────────
  async function fetchRecommendations(query) {
    setLoading(true);

    try {
      const response = await fetch('/ai/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      if (!response.ok) throw new Error('Server error');
      const data = await response.json();

      if (data.recommendations && data.recommendations.length > 0) {
        renderResults(data.recommendations, query);
        voiceStatus.textContent = `Found ${data.recommendations.length} great matches!`;
      } else {
        voiceStatus.textContent = 'No matches found. Try different words.';
      }
    } catch (err) {
      console.error(err);
      voiceStatus.textContent = '⚠️ Something went wrong. Please try again.';
    } finally {
      setLoading(false);
    }
  }

  // ── Render result cards ────────────────────────────────
  function renderResults(cafes, query) {
    resultsQuery.textContent = `"${query}"`;
    resultsGrid.innerHTML = '';

    cafes.forEach((cafe, i) => {
      const img_src = `/static/images/${cafe.image}`;
      const fallback = 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&h=400&fit=crop';

      const card = document.createElement('a');
      card.href = `/cafes/${cafe.id}`;
      card.className = 'result-card';
      card.style.animationDelay = `${i * 0.1}s`;
      card.innerHTML = `
        <div class="result-card-img">
          <img src="${img_src}" alt="${cafe.name}"
               onerror="this.src='${fallback}'">
        </div>
        <div class="result-card-body">
          <p class="result-card-name">${cafe.name}</p>
          <p class="result-reason">${cafe.reason}</p>
          <span class="result-card-link">View Cafe →</span>
        </div>
      `;
      resultsGrid.appendChild(card);
    });

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // ── Loading state ─────────────────────────────────────
  function setLoading(on) {
    if (on) {
      micBtn.disabled = true;
      voiceStatus.innerHTML = `
        <span style="display:inline-flex;align-items:center;gap:8px">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
          </svg>
          Finding your perfect cafe…
        </span>`;
    } else {
      micBtn.disabled = false;
    }
  }

})();
