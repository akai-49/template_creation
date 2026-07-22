import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderHeader(block, doc, renderNode) {
  const p = block.data.props || {}
  const bg = escapeHtml(p.backgroundColor || '#ffffff')
  const rows = (block.data.childrenIds || []).map((id) => renderNode(doc, id)).join('\n')
  return `<tr>
    <td style="background-color:${bg};border-bottom:1px solid #e5e7eb;padding:${paddingCss(p)};">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rows}</table>
    </td>
  </tr>`
}
