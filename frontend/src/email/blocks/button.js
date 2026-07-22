import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

function radiusFor(style) {
  if (style === 'pill') return '999px'
  if (style === 'rectangle') return '0px'
  return '6px'
}

export function renderButton(block) {
  const p = block.data.props || {}
  const bg = escapeHtml(p.backgroundColor || '#5b21b6')
  const color = escapeHtml(p.textColor || '#ffffff')
  const url = escapeHtml(p.url || '#')
  const align = escapeHtml(p.align || 'left')
  const fontSize = escapeHtml((p.fontSize ?? 16) + 'px')
  const fontWeight = escapeHtml(p.fontWeight || 'bold')
  const radius = radiusFor(p.style)
  const widthAttr = p.width === 'full' ? ' width="100%"' : ''
  return `<tr>
    <td style="padding:${paddingCss(p)};" align="${align}">
      <table role="presentation" cellpadding="0" cellspacing="0"${widthAttr}>
        <tr>
          <td style="border-radius:${radius};background-color:${bg};" align="center">
            <a href="${url}" style="display:inline-block;width:${p.width === 'full' ? '100%' : 'auto'};box-sizing:border-box;padding:10px 20px;font-family:Arial,Helvetica,sans-serif;font-size:${fontSize};font-weight:${fontWeight};color:${color};text-decoration:none;text-align:center;">${escapeHtml(p.label)}</a>
          </td>
        </tr>
      </table>
    </td>
  </tr>`
}
