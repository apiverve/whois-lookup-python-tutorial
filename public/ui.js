// Helpers for the page script. The page only ever calls this app's own /api route;
// the API key stays on the server.

/** Calls an /api route and returns its JSON, or throws with the error message it sent. */
export async function api(path, options) {
  let res;
  try {
    res = await fetch(path, options);
  } catch {
    throw new Error('Could not reach the server. Check your connection and try again.');
  }
  const body = await res.json().catch(() => null);
  if (!res.ok) throw new Error(body?.error || `Request failed (${res.status})`);
  return body;
}

/** Escapes text for safe use inside HTML. */
export const esc = (value) =>
  String(value ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

/** Disables a button and swaps its label while work runs. */
export async function busy(button, label, work) {
  const idle = button.textContent;
  button.disabled = true;
  button.textContent = label;
  try {
    return await work();
  } finally {
    button.disabled = false;
    button.textContent = idle;
  }
}

/** Shows an error in the result area. */
export function showError(target, err) {
  target.innerHTML = `<p class="error" role="alert">${esc(err.message || err)}</p>`;
}

/** A grid of label/value pairs. Rows with an empty value are left out. */
export function stats(rows) {
  const items = rows
    .filter(([, value]) => value !== undefined && value !== null && value !== '')
    .map(([label, value]) => `<div><dt>${esc(label)}</dt><dd>${esc(value)}</dd></div>`)
    .join('');
  return `<dl class="stats">${items}</dl>`;
}

/** Turns "https://Example.com/path" into "example.com". */
export const toDomain = (value) =>
  value.trim().toLowerCase().replace(/^[a-z]+:\/\//, '').replace(/[/?#:].*$/, '').replace(/\.$/, '');
