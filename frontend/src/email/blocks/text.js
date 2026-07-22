import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderText(block) {
  const p = block.data.props || {}
  const fontSize = escapeHtml((p.fontSize ?? 16) + 'px')
  const fontWeight = escapeHtml(p.fontWeight || 'normal')
  const align = escapeHtml(p.align || 'left')
  const color = escapeHtml(p.color || '#111111')
  const bg = p.backgroundColor ? `background-color:${escapeHtml(p.backgroundColor)};` : ''
  return `<tr><td style="padding:${paddingCss(p)};font-family:Arial,Helvetica,sans-serif;font-size:${fontSize};font-weight:${fontWeight};text-align:${align};color:${color};${bg}line-height:1.5;">${escapeHtml(p.text)}</td></tr>`
}
