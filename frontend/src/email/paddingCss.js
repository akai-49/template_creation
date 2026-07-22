export function paddingCss(p = {}) {
  const t = p.paddingTop ?? 0
  const r = p.paddingRight ?? 0
  const b = p.paddingBottom ?? 0
  const l = p.paddingLeft ?? 0
  return `${t}px ${r}px ${b}px ${l}px`
}
