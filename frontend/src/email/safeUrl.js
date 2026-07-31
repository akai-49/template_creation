const HREF_SCHEMES = ['http', 'https', 'mailto', 'tel']
const SRC_SCHEMES = [...HREF_SCHEMES, 'data']
const SCHEME = /^([a-z][a-z0-9+.-]*):/i
// eslint-disable-next-line no-control-regex
const CONTROL_CHARS = /[\u0000-\u0020]/g

/**
 * Neutralises `javascript:` and friends before a value reaches an href.
 * Escaping alone doesn't help here — `javascript:alert(1)` contains nothing to escape.
 */
export function safeUrl(value, fallback = '#', allowed = HREF_SCHEMES) {
  const url = String(value ?? '').trim()
  if (!url) return fallback

  // Browsers ignore control characters when resolving a scheme, so "java\tscript:" runs.
  const scheme = SCHEME.exec(url.replace(CONTROL_CHARS, ''))
  if (!scheme) return url // relative path, anchor or query — no scheme, no injection

  return allowed.includes(scheme[1].toLowerCase()) ? url : fallback
}

export function safeSrc(value, fallback = '') {
  return safeUrl(value, fallback, SRC_SCHEMES)
}
