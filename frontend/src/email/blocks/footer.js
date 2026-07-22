import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderFooter(block, doc, renderNode) {
  const p = block.data.props || {}
  const bg = escapeHtml(p.backgroundColor || '#f5f5f5')
  const rows = (block.data.childrenIds || []).map((id) => renderNode(doc, id)).join('\n')
  const fallback = !block.data.childrenIds?.length
    ? `<tr><td style="padding:16px 24px;font-family:Arial,sans-serif;font-size:12px;color:#9ca3af;text-align:center;">${escapeHtml(p.text || '')}</td></tr>`
    : ''
  return `<tr>
    <td style="background-color:${bg};border-top:1px solid #e5e7eb;padding:${paddingCss(p)};">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rows}${fallback}</table>
    </td>
  </tr>`
}
