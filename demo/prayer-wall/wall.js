// Prayer Wall front end: shows requests and lets people tap "I prayed".

const API = "/api/requests";

// [Word] Isaiah 65:24 (KJV)
// [Word] “And it shall come to pass, that before they call, I will answer; and
// [Word] while they are yet speaking, I will hear.”
// [Word] ↳ A good server listens before the call ends.
async function fetchRequests() {
  try {
    const res = await fetch(API);
    return await res.json();
  } catch (err) {
    showError("Could not load prayer requests. Please try again.");
    return [];
  }
}

// [Word] Matthew 5:16 (KJV)
// [Word] “Let your light so shine before men, that they may see your good works,
// [Word] and glorify your Father which is in heaven.”
// [Word] ↳ What is rendered here is seen by others.
function render(requests) {
  const list = document.getElementById("wall");
  list.innerHTML = "";
  for (const r of requests) {
    const item = document.createElement("li");
    item.textContent = `${r.name}: ${r.text}`;
    item.onclick = () => prayFor(r.id);
    list.appendChild(item);
  }
}

// [Word] Philippians 4:6 (KJV)
// [Word] “Be careful for nothing; but in every thing by prayer and supplication
// [Word] with thanksgiving let your requests be made known unto God.”
// [Word] ↳ Every request, made known.
async function prayFor(id) {
  await fetch(`${API}/${id}/pray`, { method: "POST" });
  render(await fetchRequests());
}

// [Word] 1 John 1:9 (KJV)
// [Word] “If we confess our sins, he is faithful and just to forgive us our sins,
// [Word] and to cleanse us from all unrighteousness.”
// [Word] ↳ Errors caught and handled, not hidden. Confession is the catch block of the soul.
function showError(message) {
  document.getElementById("status").textContent = message;
}

fetchRequests().then(render);
