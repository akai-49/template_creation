import { renderText } from './blocks/text'
import { renderButton } from './blocks/button'
import { renderImage } from './blocks/image'
import { renderVideo } from './blocks/video'
import { renderDivider } from './blocks/divider'
import { renderSpacer } from './blocks/spacer'
import { renderSocialIcons } from './blocks/socialIcons'
import { renderFormField } from './blocks/formField'
import { renderHtmlBlock } from './blocks/html'
import { renderSection } from './blocks/section'
import { renderColumns } from './blocks/columns'
import { renderHeader } from './blocks/header'
import { renderFooter } from './blocks/footer'
import { escapeHtml } from './escapeHtml'

const FONT_STACKS = {
  'Modern sans': 'Arial, Helvetica, sans-serif',
  Serif: 'Georgia, "Times New Roman", serif',
  Monospace: '"Courier New", monospace',
}

const REGISTRY = {
  Text: renderText,
  Button: renderButton,
  Image: renderImage,
  Video: renderVideo,
  Divider: renderDivider,
  Spacer: renderSpacer,
  'Social Icons': renderSocialIcons,
  'Form Field': renderFormField,
  HTML: renderHtmlBlock,
  Section: renderSection,
  Columns: renderColumns,
  Header: renderHeader,
  Footer: renderFooter,
}

const CONTAINER_TYPES = new Set(['Section', 'Columns', 'Header', 'Footer'])

export function renderNode(doc, id) {
  const node = doc[id]
  if (!node) return ''
  const renderer = REGISTRY[node.type]
  if (!renderer) return ''
  const trHtml = renderer({ id, ...node }, doc, renderNode)

  const widthPercent = node.data.props?.widthPercent
  if (!widthPercent || widthPercent >= 100 || CONTAINER_TYPES.has(node.type)) return trHtml

  const align = escapeHtml(node.data.props?.align || 'left')
  return `<tr><td align="${align}"><table role="presentation" width="${widthPercent}%" cellpadding="0" cellspacing="0">${trHtml}</table></td></tr>`
}

export function renderDocumentToHtml(doc) {
  const style = doc.root?.data || {}
  const childrenIds = style.childrenIds || []
  const rows = childrenIds.map((id) => renderNode(doc, id)).join('\n')

  const backdrop = escapeHtml(style.backdropColor || '#f4f4f5')
  const canvasColor = escapeHtml(style.canvasColor || '#ffffff')
  const textColor = escapeHtml(style.textColor || '#111111')
  const fontFamily = FONT_STACKS[style.fontFamily] || FONT_STACKS['Modern sans']
  const border = style.canvasBorderColor
    ? `border:1px solid ${escapeHtml(style.canvasBorderColor)};`
    : ''
  const radius = `border-radius:${style.canvasBorderRadius ?? 0}px;`

  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <title>Email</title>
  </head>
  <body style="margin:0;padding:0;background-color:${backdrop};font-family:${fontFamily};color:${textColor};">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:${backdrop};">
      <tr>
        <td align="center" style="padding:24px 0;">
          <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background-color:${canvasColor};max-width:600px;width:100%;${border}${radius}">
            ${rows}
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>`
}
