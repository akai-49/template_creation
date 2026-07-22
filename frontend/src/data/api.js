import { frappeRequest } from 'frappe-ui'

const METHOD = (name) => `marketing_studio.api.template.${name}`

export function getBlockLibrary() {
  return frappeRequest({ url: `/api/method/${METHOD('get_block_library')}` })
}

export function listTemplates(params = {}) {
  return frappeRequest({
    url: `/api/method/${METHOD('list_templates')}`,
    params,
  })
}

export function getTemplate(name) {
  return frappeRequest({
    url: `/api/method/${METHOD('get_template')}`,
    params: { name },
  })
}

export function createTemplate({ title, template_type, category }) {
  return frappeRequest({
    url: `/api/method/${METHOD('create_template')}`,
    method: 'POST',
    params: { title, template_type, category },
  })
}

export function saveTemplateLayout(name, layout, preview_html) {
  return frappeRequest({
    url: `/api/method/${METHOD('save_template_layout')}`,
    method: 'POST',
    params: { name, layout: JSON.stringify(layout), preview_html },
  })
}

export function publishTemplate(name) {
  return frappeRequest({
    url: `/api/method/${METHOD('publish_template')}`,
    method: 'POST',
    params: { name },
  })
}

export function duplicateTemplate(name, title) {
  return frappeRequest({
    url: `/api/method/${METHOD('duplicate_template')}`,
    method: 'POST',
    params: { name, title },
  })
}

export function createVersion(name, version_label) {
  return frappeRequest({
    url: `/api/method/${METHOD('create_version')}`,
    method: 'POST',
    params: { name, version_label },
  })
}
