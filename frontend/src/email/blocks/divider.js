import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderDivider(block) {
  const p = block.data.props || {}
  const color = escapeHtml(p.color || '#e5e7eb')
  const thickness = escapeHtml((p.thickness ?? 1) + 'px')
  return `<tr>
    <td style="padding:${paddingCss(p)};">
      <div style="border-top:${thickness} solid ${color};line-height:0;font-size:0;">&nbsp;</div>
    </td>
  </tr>`
}
