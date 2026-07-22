import { paddingCss } from '../paddingCss'

export function renderSpacer(block) {
  const p = block.data.props || {}
  const height = (p.height ?? 24) + 'px'
  return `<tr><td style="height:${height};line-height:${height};font-size:0;padding:${paddingCss(p)};">&nbsp;</td></tr>`
}
