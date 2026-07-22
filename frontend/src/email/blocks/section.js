import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderSection(block, doc, renderNode) {
  const p = block.data.props || {}
  const bg = escapeHtml(p.backgroundColor || '#ffffff')
  const padding = paddingCss(p)
  const rows = (block.data.childrenIds || []).map((id) => renderNode(doc, id)).join('\n')
  return `<tr>
    <td style="background-color:${bg};padding:${padding};">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rows}</table>
    </td>
  </tr>`
}
