(function () {
    const STORAGE_KEY = "a0_storyboard_state";

    const poem = [
        "D is for death, for Donna drifting out of reach.",
        "D is for the dope that dulls and divides.",
        "D is for the door that closes with a whisper.",
        "D is for the dark we scan through, grain by grain."
    ].join("\n");

    let state = {
        beats: [],
        characters: [],
        ideas: [],
    };

    function writeToChat(message) {
        if (window.updateChatInput) {
            window.updateChatInput(message);
            return;
        }
        const input = document.getElementById("chat-input");
        if (!input) return;
        input.value = message;
        input.focus();
        input.dispatchEvent(new Event("input", { bubbles: true }));
    }

    function switchTab(targetId) {
        document
            .querySelectorAll(".creative-tab")
            .forEach((btn) => btn.classList.toggle("active", btn.dataset.target === targetId));
        document
            .querySelectorAll("#creative-panels .creative-panel")
            .forEach((panel) => panel.classList.toggle("hidden", panel.id !== targetId));
    }

    function loadState() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return;
            const parsed = JSON.parse(raw);
            state = {
                beats: parsed.beats || [],
                characters: parsed.characters || [],
                ideas: parsed.ideas || [],
            };
        } catch (err) {
            console.warn("[CreativeTabs] failed to load storyboard state", err);
        }
    }

    function saveState() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    function renderList(listId, items, formatter) {
        const el = document.getElementById(listId);
        if (!el) return;

        if (!items.length) {
            el.classList.add("empty-state");
            el.innerHTML = "No entries yet";
            return;
        }

        el.classList.remove("empty-state");
        el.innerHTML = items
            .map(
                (item, idx) => `
                <div class="storyboard-pill">
                    <div>
                        <div>${formatter(item)}</div>
                        ${item.meta ? `<div class="pill-meta">${item.meta}</div>` : ""}
                    </div>
                    <button class="pill-delete" data-list="${listId}" data-index="${idx}" aria-label="Delete item">×</button>
                </div>
            `
            )
            .join("");
    }

    function render() {
        renderList(
            "beat-list",
            state.beats,
            (item) => `<strong>${item.label}</strong>${item.note ? " — " + item.note : ""}`
        );
        renderList(
            "character-list",
            state.characters,
            (item) => `<strong>${item.name}</strong>${item.role ? " — " + item.role : ""}`
        );
        renderList("idea-list", state.ideas, (item) => item.note || "");
    }

    function addBeat(label, note) {
        state.beats.unshift({
            label: label.trim(),
            note: (note || "").trim(),
            meta: "Beat",
        });
        saveState();
        render();
    }

    function addCharacter(name, role) {
        state.characters.unshift({
            name: name.trim(),
            role: (role || "").trim(),
            meta: "Character",
        });
        saveState();
        render();
    }

    function addIdea(note) {
        if (!note.trim()) return;
        state.ideas.unshift({ note: note.trim(), meta: "Idea" });
        saveState();
        render();
    }

    function deleteItem(listId, index) {
        const mapping = {
            "beat-list": "beats",
            "character-list": "characters",
            "idea-list": "ideas",
        };
        const key = mapping[listId];
        if (!key || !Array.isArray(state[key])) return;
        state[key].splice(index, 1);
        saveState();
        render();
    }

    function clearList(key) {
        if (!state[key]) return;
        state[key] = [];
        saveState();
        render();
    }

    function clearAll() {
        state = { beats: [], characters: [], ideas: [] };
        saveState();
        render();
    }

    function buildStoryboardSummary() {
        const parts = [];
        if (state.beats.length) {
            parts.push(
                "Beats:",
                ...state.beats.map((b, idx) => `${idx + 1}. ${b.label}${b.note ? " — " + b.note : ""}`)
            );
        }
        if (state.characters.length) {
            parts.push(
                "Characters:",
                ...state.characters.map((c) => `- ${c.name}${c.role ? " (" + c.role + ")" : ""}`)
            );
        }
        if (state.ideas.length) {
            parts.push("Ideas:", ...state.ideas.map((i) => `• ${i.note}`));
        }
        return parts.join("\n");
    }

    function wireTabs() {
        const overlay = document.getElementById("creative-overlay");
        const closeBtn = document.getElementById("creative-close");

        document.querySelectorAll(".creative-tab").forEach((btn) => {
            btn.addEventListener("click", () => {
                overlay?.classList.remove("hidden");
                switchTab(btn.dataset.target);
            });
        });

        closeBtn?.addEventListener("click", () => overlay?.classList.add("hidden"));
        overlay?.addEventListener("click", (e) => {
            if (e.target === overlay) overlay.classList.add("hidden");
        });
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") overlay?.classList.add("hidden");
        });
    }

    function wireInspo() {
        document.getElementById("inspo-insert")?.addEventListener("click", () => writeToChat(poem));
        document.getElementById("inspo-copy")?.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(poem);
                if (window.showToast) window.showToast("Inspo copied", 2000);
            } catch (err) {
                console.warn("Clipboard unavailable", err);
            }
        });
    }

    function wireStoryboard() {
        const beatForm = document.getElementById("beat-form");
        const characterForm = document.getElementById("character-form");
        const ideaForm = document.getElementById("idea-form");
        const sendButton = document.getElementById("storyboard-send");

        beatForm?.addEventListener("submit", (e) => {
            e.preventDefault();
            const label = document.getElementById("beat-label").value || "";
            const note = document.getElementById("beat-notes").value || "";
            if (!label.trim()) return;
            addBeat(label, note);
            beatForm.reset();
        });

        characterForm?.addEventListener("submit", (e) => {
            e.preventDefault();
            const name = document.getElementById("character-name").value || "";
            const role = document.getElementById("character-role").value || "";
            if (!name.trim()) return;
            addCharacter(name, role);
            characterForm.reset();
        });

        ideaForm?.addEventListener("submit", (e) => {
            e.preventDefault();
            const note = document.getElementById("idea-notes").value || "";
            addIdea(note);
            ideaForm.reset();
        });

        document.addEventListener("click", (e) => {
            const target = e.target;
            if (!(target instanceof HTMLElement)) return;
            if (target.classList.contains("pill-delete")) {
                const listId = target.dataset.list;
                const idx = Number(target.dataset.index);
                if (!Number.isNaN(idx)) deleteItem(listId, idx);
            }
        });

        document.getElementById("storyboard-clear-beats")?.addEventListener("click", () => clearList("beats"));
        document.getElementById("storyboard-clear-characters")?.addEventListener("click", () => clearList("characters"));
        document.getElementById("storyboard-clear-ideas")?.addEventListener("click", () => clearList("ideas"));
        document.getElementById("storyboard-clear-all")?.addEventListener("click", clearAll);

        sendButton?.addEventListener("click", () => {
            const summary = buildStoryboardSummary();
            if (!summary.trim()) {
                if (window.showToast) window.showToast("Add beats, characters, or ideas first", 2000);
                return;
            }
            writeToChat(summary);
        });
    }

    document.addEventListener("DOMContentLoaded", () => {
        loadState();
        wireTabs();
        wireInspo();
        wireStoryboard();
        render();
        switchTab("creative-inspo");
    });
})();
