import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

export function renderVideo(block) {
  const p = block.data.props || {}
  const url = escapeHtml(p.url || '#')
  const padding = paddingCss(p)
  if (p.thumbnail) {
    return `<tr>
      <td style="padding:${padding};">
        <a href="${url}" style="text-decoration:none;">
          <img src="${escapeHtml(p.thumbnail)}" alt="Video" width="100%" style="width:100%;display:block;border:0;" />
        </a>
      </td>
    </tr>`
  }
  return `<tr>
    <td style="padding:${padding};">
      <a href="${url}" style="display:block;padding:40px;text-align:center;background-color:#111827;color:#ffffff;font-family:Arial,sans-serif;font-size:13px;text-decoration:none;">&#9654; Watch video</a>
    </td>
  </tr>`
}
