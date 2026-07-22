import { paddingCss } from '../paddingCss'

export function renderHtmlBlock(block) {
  const p = block.data.props || {}
  // Intentionally unescaped: this block exists as the author's raw-HTML escape hatch.
  return `<tr><td style="padding:${paddingCss(p)};">${p.html || ''}</td></tr>`
}
