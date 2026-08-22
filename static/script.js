const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
const browseBtn = document.getElementById("browse-btn");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error-box");
const results = document.getElementById("results");
const fileMeta = document.getElementById("file-meta");
const extractedText = document.getElementById("extracted-text");
const statsGrid = document.getElementById("stats-grid");
const suggestionsList = document.getElementById("suggestions-list");
const platformChips = document.querySelectorAll(".platform-chip");
const copyBtn = document.getElementById("copy-btn");
const downloadBtn = document.getElementById("download-btn");

let selectedPlatform = "general";
let lastData = null;

platformChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    platformChips.forEach((c) => c.classList.remove("active"));
    chip.classList.add("active");
    selectedPlatform = chip.dataset.platform;
  });
});

browseBtn.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  if (fileInput.files.length) {
    handleFile(fileInput.files[0]);
  }
});

["dragenter", "dragover"].forEach((evt) => {
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add("dragover");
  });
});

["dragleave", "drop"].forEach((evt) => {
  dropZone.addEventListener(evt, (e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove("dragover");
  });
});

dropZone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

function resetUI() {
  errorBox.classList.add("hidden");
  errorBox.textContent = "";
  results.classList.add("hidden");
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

async function handleFile(file) {
  resetUI();
  loading.classList.remove("hidden");

  const formData = new FormData();
  formData.append("file", file);
  formData.append("platform", selectedPlatform);

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    loading.classList.add("hidden");

    if (!response.ok) {
      showError(data.error || "Something went wrong while processing the file.");
      return;
    }

    if (data.warning) {
      showError(data.warning);
      return;
    }

    lastData = data;
    renderResults(data);
  } catch (err) {
    loading.classList.add("hidden");
    showError("Network error: could not reach the server.");
  }
}

function renderResults(data) {
  fileMeta.textContent = `${data.filename} · ${data.source_type.toUpperCase()} · Analyzed for ${data.analysis.platform}`;
  extractedText.textContent = data.extracted_text;

  const a = data.analysis;
  statsGrid.innerHTML = "";
  const stats = [
    { label: "Words", value: a.word_count },
    { label: "Characters", value: a.character_count },
    { label: "Hashtags", value: a.hashtag_count },
    { label: "Mentions", value: a.mention_count },
    { label: "Links", value: a.url_count },
    { label: "Emojis", value: a.emoji_count },
    { label: "Avg Sentence Len", value: a.avg_sentence_length },
    { label: "Read Time", value: a.reading_time },
  ];
  stats.forEach((s) => {
    const div = document.createElement("div");
    div.className = "stat";
    const isLongText = typeof s.value === "string" && s.value.length > 5;
    div.innerHTML = `<div class="value${isLongText ? " value-small" : ""}">${s.value}</div><div class="label">${s.label}</div>`;
    statsGrid.appendChild(div);
  });

  suggestionsList.innerHTML = "";
  a.suggestions.forEach((s) => {
    const li = document.createElement("li");
    li.textContent = s;
    suggestionsList.appendChild(li);
  });

  results.classList.remove("hidden");
}

copyBtn.addEventListener("click", async () => {
  if (!lastData) return;
  try {
    await navigator.clipboard.writeText(lastData.extracted_text);
    const original = copyBtn.textContent;
    copyBtn.textContent = "Copied!";
    setTimeout(() => (copyBtn.textContent = original), 1500);
  } catch (err) {
    showError("Could not copy to clipboard.");
  }
});

downloadBtn.addEventListener("click", () => {
  if (!lastData) return;
  const a = lastData.analysis;
  const lines = [
    `Social Media Content Analyzer — Report`,
    `File: ${lastData.filename}`,
    `Platform: ${a.platform}`,
    ``,
    `--- Extracted Text ---`,
    lastData.extracted_text,
    ``,
    `--- Stats ---`,
    `Words: ${a.word_count}`,
    `Characters: ${a.character_count}`,
    `Hashtags: ${a.hashtag_count} (${a.hashtags.join(", ")})`,
    `Mentions: ${a.mention_count}`,
    `Links: ${a.url_count}`,
    `Emojis: ${a.emoji_count}`,
    `Avg sentence length: ${a.avg_sentence_length}`,
    `Reading time: ${a.reading_time}`,
    ``,
    `--- Suggestions ---`,
    ...a.suggestions.map((s) => `- ${s}`),
  ];
  const blob = new Blob([lines.join("\n")], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${lastData.filename.replace(/\.[^/.]+$/, "")}-report.txt`;
  link.click();
  URL.revokeObjectURL(url);
});
