import { api, busy, esc, showError, stats, toDomain } from './ui.js';

const EXAMPLES = ['github.com', 'google.com', 'wikipedia.org', 'apiverve.com'];

const form = document.getElementById('form');
const domain = document.getElementById('domain');
const go = document.getElementById('go');
const result = document.getElementById('result');

document.getElementById('examples').innerHTML = EXAMPLES
  .map((d) => `<button type="button">${esc(d)}</button>`)
  .join('');

document.getElementById('examples').addEventListener('click', (e) => {
  const chip = e.target.closest('button');
  if (!chip) return;
  domain.value = chip.textContent;
  form.requestSubmit();
});

const day = (value) => {
  const date = value ? new Date(value) : null;
  return date && !isNaN(date) ? date.toLocaleDateString(undefined, { dateStyle: 'medium' }) : null;
};

function expiry(value) {
  const date = value ? new Date(value) : null;
  if (!date || isNaN(date)) return null;
  const days = Math.floor((date - Date.now()) / 86400000);
  return days < 0 ? `${day(value)} (expired)` : `${day(value)} (in ${days.toLocaleString()} days)`;
}

// Statuses arrive as "client transfer prohibited https://icann.org/epp#client transfer prohibited";
// keep the words before the link.
const statusText = (s) => String(s).replace(/\s*https?:\/\/.*$/, '');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const name = toDomain(domain.value);
  busy(go, 'Looking up…', async () => {
    try {
      const d = await api(`/api/whois?${new URLSearchParams({ domain: name })}`);
      if (!d.createdDate && !d.registrar) {
        result.innerHTML = `<p class="hint">No WHOIS record for ${esc(d.domain || name)}. It may not be registered, or its registry doesn’t publish WHOIS data.</p>`;
        return;
      }
      const servers = (d.nameServers || []).map((s) => s.toLowerCase());
      const statuses = (d.domainStatus || []).map(statusText).filter(Boolean);
      const age = typeof d.domainAgeYears === 'number' ? `${d.domainAgeYears} years` : null;
      result.innerHTML = `
        <div class="figure">
          <div class="big">${esc(d.domain || name)}</div>
          <div class="sub">${d.registrar ? `Registered with ${esc(d.registrar)}` : 'Registrar not listed'}${age ? `, ${esc(age)} ago` : ''}</div>
        </div>
        ${stats([
          ['Registered', day(d.createdDate)],
          ['Expires', expiry(d.expiryDate)],
          ['Last updated', day(d.updatedDate)],
          ['DNSSEC', d.dNSSEC],
          ['Trust score', typeof d.trustScore === 'number' ? `${d.trustScore} / 100` : null]
        ])}
        ${servers.length ? `<h2>Name servers</h2><ul class="list mono">${servers.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>` : ''}
        ${statuses.length ? `<h2>Status</h2><ul class="list">${statuses.map((s) => `<li>${esc(s)}</li>`).join('')}</ul>` : ''}`;
    } catch (err) {
      showError(result, err);
    }
  });
});
