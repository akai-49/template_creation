import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TextBlock from './TextBlock.vue'
import HtmlBlock from './HtmlBlock.vue'
import ImageBlock from './ImageBlock.vue'

const block = (props) => ({ block: { id: 'b1', type: 'Text', data: { props } } })

describe('canvas blocks', () => {
  it('renders text as text, never as markup', () => {
    const wrapper = mount(TextBlock, { props: block({ text: '<b>bold</b>' }) })
    expect(wrapper.text()).toContain('<b>bold</b>')
    expect(wrapper.find('b').exists()).toBe(false)
  })

  it('does not execute a Custom HTML block on the canvas', () => {
    const wrapper = mount(HtmlBlock, { props: block({ html: '<img onerror="alert(1)">' }) })
    expect(wrapper.html()).not.toContain('onerror')
  })

  it('falls back to a placeholder when an image has no source', () => {
    expect(mount(ImageBlock, { props: block({}) }).text()).toContain('Image placeholder')
    expect(
      mount(ImageBlock, { props: block({ src: 'https://x/y.png', alt: 'Y' }) })
        .find('img')
        .attributes('alt'),
    ).toBe('Y')
  })

  it('tolerates a block with no props at all', () => {
    const wrapper = mount(TextBlock, {
      props: { block: { id: 'b1', type: 'Text', data: {} } },
    })
    expect(wrapper.exists()).toBe(true)
  })
})
