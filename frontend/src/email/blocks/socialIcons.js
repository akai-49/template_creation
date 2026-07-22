import { escapeHtml } from '../escapeHtml'
import { paddingCss } from '../paddingCss'

const NETWORKS = ['facebook', 'twitter', 'instagram', 'linkedin']

export function renderSocialIcons(block) {
  const p = block.data.props || {}
  const cells = NETWORKS.filter((n) => p[n])
    .map(
      (network) =>
        `<td style="padding:0 8px;"><a href="${escapeHtml(p[network])}" style="font-family:Arial,sans-serif;font-size:12px;color:#6b7280;text-decoration:none;">${escapeHtml(network)}</a></td>`,
    )
    .join('')

  return `<tr>
    <td style="padding:${paddingCss(p)};">
      <table role="presentation" cellpadding="0" cellspacing="0"><tr>${cells}</tr></table>
    </td>
  </tr>`
}
