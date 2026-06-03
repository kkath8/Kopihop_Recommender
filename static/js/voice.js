/*
 * voice.js — KopiHop Pure Voice Assistant
 */

(function () {
  "use strict";

  // DOM
  const micBtn         = document.getElementById("micBtn");
  const micRing        = document.getElementById("micRing");
  const micStatus      = document.getElementById("micStatus");
  const transcript     = document.getElementById("transcript");
  const resultsSection = document.getElementById("resultsSection");
  const resultsGrid    = document.getElementById("resultsGrid");
  const aiSpeechBubble = document.getElementById("aiSpeechBubble");
  const aiSpeechText   = document.getElementById("aiSpeechText");
  const engineBadge    = document.getElementById("engineBadge");

  // State
  let isListening         = false;
  let isSpeaking          = false;
  let finalTranscript     = "";
  let autoSubmitTimer     = null;
  let conversationHistory = [];

  // Restore previous results on page load (fixes back-button bug)
  (function restoreState() {
    try {
      const saved = sessionStorage.getItem("kopihop_last");
      if (!saved) return;
      const state = JSON.parse(saved);
      if (state.recommendations && state.recommendations.length) {
        if (state.query && transcript) {
          transcript.textContent = state.query;
          transcript.classList.remove("empty");
        }
        if (state.ai_message && aiSpeechBubble && aiSpeechText) {
          aiSpeechText.textContent = state.ai_message;
          aiSpeechBubble.classList.add("visible");
        }
        if (engineBadge && state.engine) {
          engineBadge.textContent = state.engine === "ollama" ? "🤖 AI" : "🔍︎ Smart Search";
          engineBadge.style.display = "inline-block";
        }
        renderCards(state.recommendations, false); // false = don't scroll on restore
      }
    } catch (e) { /* ignore */ }
  })();

  // Speech Recognition
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SR) {
    micStatus.textContent = "Voice not supported. Use Chrome or Edge.";
    micBtn.disabled = true;
    return;
  }

  const recognition           = new SR();
  recognition.lang            = "en-PH";
  recognition.interimResults  = true;
  recognition.maxAlternatives = 1;
  recognition.continuous      = false;

  // Mic Button 
  micBtn.addEventListener("click", () => {
    if (isSpeaking) { stopSpeaking(); return; }
    if (isListening) { recognition.stop(); } else { startListening(); }
  });

  function startListening() {
    finalTranscript = "";
    transcript.textContent = "";
    transcript.classList.add("empty");
    hideResults();
    hideAiBubble();
    if (engineBadge) engineBadge.style.display = "none";
    sessionStorage.removeItem("kopihop_last"); // clear saved state for new search
    recognition.start();
  }

  // Recognition Events
  recognition.onstart = () => {
    isListening = true;
    setMicState("listening");
    micStatus.textContent = "Listening… speak now";
  };

  recognition.onresult = (e) => {
    let interim = "";
    finalTranscript = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const t = e.results[i][0].transcript;
      e.results[i].isFinal ? (finalTranscript += t) : (interim += t);
    }
    transcript.textContent = finalTranscript || interim;
    if (transcript.textContent.trim()) transcript.classList.remove("empty");

    if (finalTranscript) {
      clearTimeout(autoSubmitTimer);
      autoSubmitTimer = setTimeout(() => recognition.stop(), 1500);
    }
  };

  recognition.onerror = (e) => {
    isListening = false;
    setMicState("idle");
    const msgs = {
      "no-speech":   "Didn't catch that. Tap and try again.",
      "not-allowed": "Microphone blocked. Allow it in browser settings.",
      "network":     "Network error. Check your connection.",
    };
    micStatus.textContent = msgs[e.error] || "Error: " + e.error;
  };

  recognition.onend = () => {
    isListening = false;
    const query = finalTranscript.trim();
    if (query.length > 2) {
      setMicState("thinking");
      fetchRecommendations(query, "voice");
    } else {
      setMicState("idle");
      micStatus.textContent = query ? "Say a bit more and try again." : "Tap the mic to start.";
    }
  };

  // Fetch Recommendations
  async function fetchRecommendations(query, inputMethod) {
    try {
      const res = await fetch("/ai/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          input_method:         inputMethod || "voice",
          conversation_history: conversationHistory,
        }),
      });

      if (!res.ok) throw new Error("Server error");
      const data = await res.json();

      conversationHistory.push({ role: "user",      content: query });
      conversationHistory.push({ role: "assistant", content: data.ai_message || "" });
      if (conversationHistory.length > 16) conversationHistory = conversationHistory.slice(-16);

      // Save full state to sessionStorage so back-button works
      try {
        sessionStorage.setItem("kopihop_last", JSON.stringify({
          query,
          ai_message:      data.ai_message || "",
          recommendations: data.recommendations || [],
          engine:          data.engine || "keyword",
        }));
      } catch (e) { /* quota exceeded — ignore */ }

      // Show AI bubble then speak
      if (data.ai_message) {
        showAiBubble(data.ai_message);
        speak(data.ai_message, () => {
          if (data.recommendations?.length) {
            renderCards(data.recommendations, true);
            const count = data.recommendations.length;
            const countMsg = count === 1
              ? "Found 1 cafe for you."
              : `Found ${count} cafes for you.`;
            speak(countMsg);
          } else {
            speak("Sorry, I couldn't find a match. Try saying something different!");
          }
          setMicState("idle");
          micStatus.textContent = "Tap the mic to search again.";
        });
      } else {
        if (data.recommendations?.length) renderCards(data.recommendations, true);
        setMicState("idle");
        micStatus.textContent = "Tap the mic to search again.";
      }

      if (engineBadge) {
        engineBadge.textContent = data.engine === "ollama" ? "🤖 AI" : "🔍︎ Smart Search";
        engineBadge.style.display = "inline-block";
      }

    } catch (err) {
      console.error(err);
      speak("Something went wrong. Please try again.");
      setMicState("idle");
      micStatus.textContent = "Error. Try again.";
    }
  }

  // Expose so chips in home.html can call it
  window.kopihopFetch = fetchRecommendations;

  // Render Cafe Cards
  function renderCards(cafes, shouldScroll) {
    resultsGrid.innerHTML = "";
    const fallback = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&h=400&fit=crop";

    cafes.forEach((cafe, i) => {
      const card = document.createElement("a");
      card.href      = `/cafes/${cafe.id}`;
      card.className = "result-card";
      card.style.animationDelay = `${i * 0.08}s`;
      card.innerHTML = `
        <div class="rc-img">
          <img src="/static/images/${esc(cafe.image)}" alt="${esc(cafe.name)}"
               onerror="this.src='${fallback}'">
        </div>
        <div class="rc-body">
          <div class="rc-top">
            <span class="rc-name">${esc(cafe.name)}</span>
            <span class="rc-price">${esc(cafe.price_range || "")}</span>
          </div>
          <p class="rc-reason">${esc(cafe.reason)}</p>
          <p class="rc-hours">🕐 ${esc(cafe.hours || "Check cafe for hours")}</p>
          <span class="rc-cta">View Cafe →</span>
        </div>`;
      resultsGrid.appendChild(card);
    });

    resultsSection.style.display = "block";
    if (shouldScroll) {
      resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  // TTS
  function speak(text, onDone) {
    if (!window.speechSynthesis) { onDone && onDone(); return; }
    window.speechSynthesis.cancel();
    const utt   = new SpeechSynthesisUtterance(text);
    utt.lang    = "en-PH";
    utt.rate    = 0.93;
    utt.pitch   = 1.05;
    const voices = window.speechSynthesis.getVoices();
    const pick   = voices.find(v =>
      v.lang === "en-PH" ||
      v.lang.startsWith("fil") ||
      v.lang.startsWith("tl") ||
      (v.lang.startsWith("en") && /female|zira|samantha/i.test(v.name))
    );
    if (pick) utt.voice = pick;
    utt.onstart = () => { isSpeaking = true;  setMicState("speaking"); };
    utt.onend   = () => { isSpeaking = false; onDone && onDone(); };
    utt.onerror = () => { isSpeaking = false; onDone && onDone(); };
    window.speechSynthesis.speak(utt);
  }

  function stopSpeaking() {
    window.speechSynthesis.cancel();
    isSpeaking = false;
    setMicState("idle");
    micStatus.textContent = "Tap the mic to start.";
  }

  if (window.speechSynthesis) {
    window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();
  }

  // AI Bubble
  function showAiBubble(text) {
    if (!aiSpeechBubble) return;
    aiSpeechText.textContent = text;
    aiSpeechBubble.classList.add("visible");
  }
  function hideAiBubble() {
    if (!aiSpeechBubble) return;
    aiSpeechBubble.classList.remove("visible");
  }

  // State machine
  function setMicState(state) {
    micBtn.dataset.state  = state;
    micRing.dataset.state = state;
    const labels = {
      idle:      "Tap to speak",
      listening: "Listening…",
      thinking:  "Thinking…",
      speaking:  "Tap to stop",
    };
    micStatus.textContent = labels[state] || "";
  }

  function hideResults() { resultsSection.style.display = "none"; }

  function esc(s) {
    return String(s || "")
      .replace(/&/g,"&amp;").replace(/</g,"&lt;")
      .replace(/>/g,"&gt;").replace(/"/g,"&quot;");
  }

  setMicState("idle");

})();
