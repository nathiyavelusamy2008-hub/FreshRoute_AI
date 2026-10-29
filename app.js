const $ = (id) => document.getElementById(id);
const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

async function loadImpact() {
  try {
    const [impact, partners] = await Promise.all([
      fetch('/api/impact').then(r => r.json()),
      fetch('/api/partners').then(r => r.json())
    ]);
    $('active').textContent = impact.active_listings;
    $('listed').textContent = impact.food_units_listed.toLocaleString();
    $('rescued').textContent = impact.food_units_rescued.toLocaleString();
    $('partners').textContent = partners.length;
  } catch { ['active','listed','rescued','partners'].forEach(id => $(id).textContent = '—'); }
}

function listingCard(item) {
  const urgency = item.priority_label.toLowerCase();
  return `<article class="listing-card">
    <div class="card-top"><span class="category">${escapeHtml(item.category)}</span><span class="priority ${urgency}">${escapeHtml(item.priority_label)} · ${item.priority}/100</span></div>
    <h3>${escapeHtml(item.food_name)}</h3>
    <div class="listing-meta">
      <div>Quantity<b>${item.quantity} ${escapeHtml(item.unit)}</b></div>
      <div>Time remaining<b>${escapeHtml(item.hours_left)} hours</b></div>
      <div>Pickup location<b>⌖ ${escapeHtml(item.location)}</b></div>
      <div>Status<b>${escapeHtml(item.status)}</b></div>
    </div>
    <p class="muted">${escapeHtml(item.notes || 'No extra pickup notes provided.')}</p>
    <div class="card-bottom"><span class="donor">Listed by ${escapeHtml(item.donor)}</span><button class="match-btn" data-match="${item.id}">Find partners ↗</button></div>
    <div class="match-slot" id="matches-${item.id}"></div>
  </article>`;
}

async function loadListings() {
  const grid = $('listing-grid');
  grid.innerHTML = '<div class="empty">Loading listings…</div>';
  try {
    const items = await fetch('/api/listings').then(r => { if(!r.ok) throw new Error(); return r.json(); });
    grid.innerHTML = items.length ? items.map(listingCard).join('') : '<div class="empty">No listings yet. Add the first one below.</div>';
    grid.querySelectorAll('[data-match]').forEach(btn => btn.addEventListener('click', () => loadMatches(btn.dataset.match)));
  } catch {
    grid.innerHTML = '<div class="empty">Could not load listings. Make sure the FastAPI server is running.</div>';
  }
}

async function loadMatches(id) {
  const slot = $(`matches-${id}`);
  slot.innerHTML = '<div class="match-results">Finding suitable partners…</div>';
  try {
    const matches = await fetch(`/api/matches/${id}`).then(r => r.json());
    slot.innerHTML = `<div class="match-results"><b>Suggested partners</b><br>${matches.length ? matches.slice(0,3).map(p => `${escapeHtml(p.name)} · ${escapeHtml(p.location)} · ${p.match_score}% match`).join('<br>') : 'No close matches yet. Try another location or category.'}<br><small>Suggestions are demo matches; contact partners to confirm pickup.</small></div>`;
  } catch { slot.innerHTML = '<div class="match-results">Could not load partner matches.</div>'; }
}

$('donation-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const data = Object.fromEntries(new FormData(form).entries());
  data.quantity = Number(data.quantity);
  data.hours_left = Number(data.hours_left);
  const message = $('form-message');
  message.textContent = 'Publishing listing…';
  try {
    const response = await fetch('/api/listings', {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail?.[0]?.msg || result.detail || 'Please check the form fields.');
    message.textContent = 'Listing published successfully. It is now available in the food listings.';
    form.reset();
    await Promise.all([loadImpact(), loadListings()]);
    $('listings').scrollIntoView({behavior:'smooth'});
  } catch (error) { message.textContent = `Could not publish listing: ${error.message}`; }
});

$('refresh').addEventListener('click', () => { loadImpact(); loadListings(); });
loadImpact();
loadListings();
