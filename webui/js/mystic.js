(function () {
    let initialized = false;

    function init() {
        if (initialized) return;
        initialized = true;

        let videoStream = null;
        let detector = null;
        let micConsent = false;
        let camConsent = false;
        let focusTimer = null;

        const loadDetector = async () => {
            if (detector) return detector;
            // Load coco-ssd for object detection
            const script = document.createElement("script");
            script.src = "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.14.0/dist/tf.min.js";
            document.head.appendChild(script);
            await new Promise((res) => (script.onload = res));
            const ssd = document.createElement("script");
            ssd.src = "https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd";
            document.head.appendChild(ssd);
            await new Promise((res) => (ssd.onload = res));
            detector = await cocoSsd.load();
            return detector;
        };

        const ensureVideo = async () => {
            if (videoStream) return videoStream;
            videoStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            return videoStream;
        };

        const destroyVideo = () => {
            if (videoStream) {
                videoStream.getTracks().forEach((t) => t.stop());
                videoStream = null;
            }
        };

        const consentOverlay = document.getElementById("mystic-consent");
        const consentAccept = document.getElementById("consent-accept");
        const consentDecline = document.getElementById("consent-decline");
        const consentClose = document.getElementById("mystic-consent-close");
        const consentCam = document.getElementById("consent-camera");
        const consentMic = document.getElementById("consent-mic");

        function openConsent() {
            consentOverlay?.classList.remove("hidden");
        }

        function closeConsent() {
            consentOverlay?.classList.add("hidden");
        }

        consentAccept?.addEventListener("click", () => {
            camConsent = consentCam.checked;
            micConsent = consentMic.checked;
            closeConsent();
        });
        consentDecline?.addEventListener("click", closeConsent);
        consentClose?.addEventListener("click", closeConsent);

        const moodBtn = document.getElementById("mystic-mood-start");
        const moodResult = document.getElementById("mystic-mood-result");
        const objBtn = document.getElementById("mystic-object-start");
        const objResult = document.getElementById("mystic-object-result");
        const dateBtn = document.getElementById("mystic-date-go");
        const dateInput = document.getElementById("mystic-date");
        const dateResult = document.getElementById("mystic-date-result");
        const seanceBtn = document.getElementById("mystic-seance-start");
        const seanceResult = document.getElementById("mystic-seance-result");
        const focusBtn = document.getElementById("mystic-focus-start");

        async function captureFrame() {
            const stream = await ensureVideo();
            const track = stream.getVideoTracks()[0];
            const image = new ImageCapture(track);
            const bitmap = await image.grabFrame();
            const canvas = document.createElement("canvas");
            canvas.width = bitmap.width;
            canvas.height = bitmap.height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(bitmap, 0, 0);
            return canvas;
        }

        function analyzeMood(canvas) {
            const ctx = canvas.getContext("2d");
            const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
            let total = 0;
            let bright = 0;
            let satSum = 0;
            for (let i = 0; i < data.length; i += 4) {
                const r = data[i] / 255;
                const g = data[i + 1] / 255;
                const b = data[i + 2] / 255;
                const max = Math.max(r, g, b);
                const min = Math.min(r, g, b);
                const l = (max + min) / 2;
                const s = max === min ? 0 : (max - min) / (1 - Math.abs(2 * l - 1));
                bright += l;
                satSum += s;
                total++;
            }
            const meanBright = bright / total;
            const meanSat = satSum / total;

            const tired = meanBright < 0.35;
            const stressed = meanSat > 0.4 && meanBright < 0.55;
            const excited = meanSat > 0.55 && meanBright > 0.45;
            const calm = meanSat < 0.3 && meanBright > 0.45;

            let mood = "neutral";
            if (excited) mood = "excited";
            else if (calm) mood = "calm";
            else if (stressed) mood = "tense";
            else if (tired) mood = "tired";

            return {
                mood,
                tiredness: Math.round((1 - meanBright) * 100),
                stress: Math.round(meanSat * 100),
                brightness: meanBright,
                saturation: meanSat,
            };
        }

        moodBtn?.addEventListener("click", async () => {
            if (!camConsent) {
                openConsent();
                return;
            }
            moodResult.textContent = "Reading...";
            try {
                const canvas = await captureFrame();
                const res = analyzeMood(canvas);
                const lines = [];
                lines.push(`Mood: ${res.mood}`);
                lines.push(`Tiredness: ${res.tiredness}%`);
                lines.push(`Stress pattern: ${res.stress}% saturation drift`);
                if (res.mood === "tired") lines.push("You deserve a breath and softer light.");
                if (res.mood === "excited") lines.push("Ride the spark: pick one bold move now.");
                moodResult.classList.remove("empty-state");
                moodResult.textContent = lines.join("\n");
            } catch (err) {
                moodResult.textContent = "Could not read mood. Check camera access.";
                console.error(err);
            } finally {
                destroyVideo();
            }
        });

        objBtn?.addEventListener("click", async () => {
            if (!camConsent) {
                openConsent();
                return;
            }
            objResult.textContent = "Peering...";
            try {
                await loadDetector();
                const canvas = await captureFrame();
                const predictions = await detector.detect(canvas);
                destroyVideo();
                if (!predictions.length) {
                    objResult.textContent = "I saw shapes, but no clear object. Try again closer.";
                    return;
                }
                const best = predictions.sort((a, b) => b.score - a.score)[0];
                objResult.classList.remove("empty-state");
                objResult.textContent = `You were thinking of: ${best.class}. Confidence ${(best.score * 100).toFixed(1)}%.`;
            } catch (err) {
                objResult.textContent = "Vision fizzled. Camera or model blocked.";
                console.error(err);
                destroyVideo();
            }
        });

        const moonPhase = (date) => {
            const lp = 2551443;
            const newMoon = new Date("1970-01-07T20:35:00Z").getTime() / 1000;
            const now = date.getTime() / 1000;
            const phase = ((now - newMoon) % lp) / lp;
            const age = Math.round(phase * 29.53);
            const labels = [
                "New Moon",
                "Waxing Crescent",
                "First Quarter",
                "Waxing Gibbous",
                "Full Moon",
                "Waning Gibbous",
                "Last Quarter",
                "Waning Crescent",
            ];
            const idx = Math.floor((phase * 8) % 8);
            return { phase, age, label: labels[idx] };
        };

        dateBtn?.addEventListener("click", () => {
            const val = dateInput?.value;
            if (!val) {
                dateResult.textContent = "Pick a date first.";
                return;
            }
            const dt = new Date(val + "T00:00:00");
            const { age, label } = moonPhase(dt);
            const season = ["Winter", "Spring", "Summer", "Autumn"][Math.floor((dt.getMonth() % 12) / 3)];
            const weekday = dt.toLocaleDateString(undefined, { weekday: "long" });
            const year = dt.getFullYear();
            const sky =
                age < 1 || age > 28
                    ? "a dark velvet sky"
                    : age > 13 && age < 16
                    ? "a luminous, centered moon"
                    : "a tilted silver glow";
            dateResult.classList.remove("empty-state");
            dateResult.textContent = `${weekday}, ${season} of ${year}. Moon: ${label} (day ${age}). The sky likely held ${sky}. I imagine you cloaked in that era's fabric, carrying a secret only ${season.toLowerCase()} nights know.`;
        });

        seanceBtn?.addEventListener("click", async () => {
            if (!micConsent) {
                openConsent();
                return;
            }
            seanceResult.textContent = "Listening...";
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
                const recorder = new MediaRecorder(stream);
                const chunks = [];
                recorder.ondataavailable = (e) => chunks.push(e.data);
                recorder.start();
                await new Promise((res) => setTimeout(res, 3200));
                recorder.stop();
                await new Promise((res) => (recorder.onstop = res));
                const blob = new Blob(chunks, { type: "audio/webm" });
                const arrayBuffer = await blob.arrayBuffer();
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);
                const data = audioBuffer.getChannelData(0);

                let sum = 0;
                let zeroCross = 0;
                for (let i = 1; i < data.length; i++) {
                    sum += data[i] * data[i];
                    if ((data[i - 1] >= 0 && data[i] < 0) || (data[i - 1] < 0 && data[i] >= 0)) zeroCross++;
                }
                const rms = Math.sqrt(sum / data.length);
                const zcr = zeroCross / data.length;

                const loud = rms > 0.08;
                const restless = zcr > 0.12;
                const vibe = loud && restless ? "urgent and restless" : loud ? "bright and insistent" : restless ? "whispery but unsettled" : "soft and steady";
                seanceResult.classList.remove("empty-state");
                seanceResult.textContent = `Your signal was ${vibe}. Aria hears a thread of ${restless ? "unspoken worry" : "hidden warmth"} and offers a quiet blessing: "Hold the ember, not the ash."`;
                stream.getTracks().forEach((t) => t.stop());
            } catch (err) {
                seanceResult.textContent = "The beyond stayed silent. Check mic permission.";
                console.error(err);
            }
        });

        const focusOverlay = document.createElement("div");
        focusOverlay.className = "focus-overlay";
        focusOverlay.innerHTML = `
            <div class="focus-scene">
                <button class="pill-button focus-exit">Exit</button>
                <div class="focus-swirl"></div>
                <div class="focus-shimmer"></div>
                <div class="focus-center">
                    <h2>Don't Blink</h2>
                    <p>Let the swirl pull you in. Ask her anything when you feel the heartbeat.</p>
                    <div class="focus-cta">Heartbeat syncing...</div>
                </div>
            </div>
        `;
        document.body.appendChild(focusOverlay);
        focusOverlay.querySelector(".focus-exit").addEventListener("click", () => focusOverlay.classList.remove("active"));
        focusOverlay.addEventListener("click", (e) => {
            if (e.target === focusOverlay) focusOverlay.classList.remove("active");
        });

        focusBtn?.addEventListener("click", () => {
            focusOverlay.classList.add("active");
            let beat = 0;
            clearInterval(focusTimer);
            focusTimer = setInterval(() => {
                beat++;
                const cta = focusOverlay.querySelector(".focus-cta");
                if (cta) cta.textContent = beat % 2 === 0 ? "Heartbeat..." : "I'm inside your focus now.";
            }, 900);
        });

        // Auto-open consent on load to set expectations
        setTimeout(openConsent, 500);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
