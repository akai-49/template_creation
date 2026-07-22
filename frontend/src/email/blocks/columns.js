import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderColumns(block, doc, renderNode) {
  const p = block.data.props || {}
  const bg = escapeHtml(p.backgroundColor || '#ffffff')
  const childIds = block.data.childrenIds || []
  const widthPct = childIds.length ? (100 / childIds.length).toFixed(2) : 100
  const halfGap = (p.gap ?? 16) / 2

  const cells = childIds
    .map(
      (id) => `<td valign="top" style="width:${widthPct}%;padding:0 ${halfGap}px;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0">${renderNode(doc, id)}</table>
      </td>`,
    )
    .join('')

  return `<tr>
    <td style="background-color:${bg};padding:${paddingCss(p)};">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>${cells}</tr></table>
    </td>
  </tr>`
}
