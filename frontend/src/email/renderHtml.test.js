import { describe, it, expect } from 'vitest'
import { renderDocumentToHtml } from './renderHtml'
import { safeUrl, safeSrc } from './safeUrl'

function docWith(node) {
  return {
    root: { type: 'EmailLayout', data: { childrenIds: ['blk'] } },
    blk: node,
  }
}

describe('safeUrl', () => {
  it('keeps ordinary links', () => {
    expect(safeUrl('https://example.com/a?b=1')).toBe('https://example.com/a?b=1')
    expect(safeUrl('mailto:a@b.com')).toBe('mailto:a@b.com')
    expect(safeUrl('/relative/path')).toBe('/relative/path')
    expect(safeUrl('#anchor')).toBe('#anchor')
  })

  it('drops script-bearing schemes, including obfuscated ones', () => {
    expect(safeUrl('javascript:alert(1)')).toBe('#')
    expect(safeUrl('JaVaScRiPt:alert(1)')).toBe('#')
    expect(safeUrl('java\tscript:alert(1)')).toBe('#')
    expect(safeUrl(' javascript:alert(1)')).toBe('#')
    expect(safeUrl('vbscript:msgbox(1)')).toBe('#')
    expect(safeUrl('data:text/html,<script>alert(1)</script>')).toBe('#')
  })

  it('allows data: for image sources only', () => {
    expect(safeSrc('data:image/png;base64,AAA')).toBe('data:image/png;base64,AAA')
    expect(safeSrc('javascript:alert(1)')).toBe('')
  })
})

describe('renderDocumentToHtml', () => {
  it('escapes text content instead of emitting markup', () => {
    const html = renderDocumentToHtml(
      docWith({ type: 'Text', data: { props: { text: '<script>alert(1)</script>' } } }),
    )
    expect(html).not.toContain('<script>')
    expect(html).toContain('&lt;script&gt;')
  })

  it('neutralises a javascript: button URL', () => {
    const html = renderDocumentToHtml(
      docWith({
        type: 'Button',
        data: { props: { label: 'Go', url: 'javascript:alert(1)' } },
      }),
    )
    expect(html).not.toContain('javascript:')
    expect(html).toContain('href="#"')
  })

  it('escapes style values so a colour cannot break out of the attribute', () => {
    const html = renderDocumentToHtml(
      docWith({
        type: 'Text',
        data: { props: { text: 'hi', color: '#fff" onload="alert(1)' } },
      }),
    )
    expect(html).not.toContain('onload="alert(1)"')
  })

  it('renders an empty document without throwing', () => {
    expect(renderDocumentToHtml({ root: { type: 'EmailLayout', data: {} } })).toContain(
      '<!doctype html>',
    )
  })

  it('skips unknown block types rather than crashing', () => {
    expect(renderDocumentToHtml(docWith({ type: 'Nonsense', data: { props: {} } }))).toContain(
      '<!doctype html>',
    )
  })
})
