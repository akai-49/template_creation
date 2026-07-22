import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderFormField(block) {
  const p = block.data.props || {}
  const required = p.required ? ' *' : ''
  return `<tr>
    <td style="padding:${paddingCss(p)};font-family:Arial,sans-serif;">
      <label style="display:block;font-size:12px;font-weight:bold;color:#374151;margin-bottom:4px;">${escapeHtml(p.label)}${required}</label>
      <input type="text" name="${escapeHtml(p.label)}" placeholder="${escapeHtml(p.placeholder)}" style="width:100%;box-sizing:border-box;padding:8px;font-size:14px;border:1px solid #d1d5db;border-radius:4px;" />
    </td>
  </tr>`
}
