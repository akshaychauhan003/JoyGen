const form = document.getElementById("recommendForm");
const results = document.getElementById("results");
const statusText = document.getElementById("statusText");

function renderEmpty(message) {
  results.innerHTML = `<div class="empty">${message}</div>`;
}

function difficultyClass(level) {
  return String(level).toLowerCase();
}

function createCard(item) {
  return `
    <article class="card">
      <div class="card-top">
        <h4>${item.title}</h4>
        <span class="badge ${difficultyClass(item.difficulty)}">${item.difficulty}</span>
      </div>
      <p class="desc">${item.description}</p>
      <p class="meta"><strong>Domains:</strong> ${item.domains.join(", ")}</p>
      <p class="meta"><strong>Skills:</strong> ${item.skills.join(", ")}</p>
      <p class="meta"><strong>Estimated time:</strong> ${item.time_weeks} week(s)</p>
      <p class="reason"><strong>Why recommended:</strong> ${item.reason}</p>
    </article>
  `;
}

renderEmpty("Fill the form and generate project ideas.");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    interests: document.getElementById("interests").value.trim(),
    skill_level: document.getElementById("skill_level").value,
    known_skills: document.getElementById("known_skills").value.trim(),
    duration_weeks: Number(document.getElementById("duration_weeks").value)
  };

  if (!payload.interests) {
    statusText.textContent = "Interests are required.";
    renderEmpty("Please enter your interests first.");
    return;
  }

  statusText.textContent = "Generating recommendations...";
  results.innerHTML = "";

  try {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!data.recommendations || data.recommendations.length === 0) {
      statusText.textContent = "No matches found.";
      renderEmpty("No recommendations found. Try broader interests or more skills.");
      return;
    }

    statusText.textContent = `${data.recommendations.length} ideas generated`;
    results.innerHTML = data.recommendations.map(createCard).join("");
  } catch (error) {
    console.error(error);
    statusText.textContent = "Server error";
    renderEmpty("Could not connect to the backend. Make sure FastAPI is running.");
  }
});
