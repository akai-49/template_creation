import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderImage(block) {
  const p = block.data.props || {}
  const width = escapeHtml((p.width ?? 100) + '%')
  const align = escapeHtml(p.align || 'center')
  const padding = paddingCss(p)
  if (!p.src) {
    return `<tr><td style="padding:${padding};font-family:Arial,sans-serif;font-size:12px;color:#9ca3af;background-color:#f3f4f6;text-align:center;">Image placeholder</td></tr>`
  }
  return `<tr>
    <td style="padding:${padding};text-align:${align};">
      <img src="${escapeHtml(p.src)}" alt="${escapeHtml(p.alt)}" width="100%" style="width:${width};max-width:100%;display:inline-block;border:0;" />
    </td>
  </tr>`
}
