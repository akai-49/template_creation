import { frappeRequest, toast } from 'frappe-ui'

const METHOD = (name) => `marketing_studio.api.template.${name}`

/** Describes a failed request in terms of what the user was trying to do. */
export function describeError(error, action) {
  if (error?.exc_type === 'PermissionError') {
    return `You don't have permission to ${action}.`
  }
  const detail = error?.messages?.[0] || error?.message || ''
  if (!detail || /failed to fetch|network|load failed/i.test(detail)) {
    return `Couldn't ${action} — check your connection and try again.`
  }
  return `Couldn't ${action}: ${detail}`
}

/** Every call goes through here so no API failure can fail silently. */
function call(action, options) {
  return frappeRequest(options).catch((error) => {
    toast.error(describeError(error, action))
    throw error
  })
}

export function getBlockLibrary() {
  return call('load the block library', {
    url: `/api/method/${METHOD('get_block_library')}`,
  })
}

export function listTemplates(params = {}) {
  return call('load templates', {
    url: `/api/method/${METHOD('list_templates')}`,
    params,
  })
}

export function getTemplate(name) {
  return call('open this template', {
    url: `/api/method/${METHOD('get_template')}`,
    params: { name },
  })
}

export function createTemplate({ title, template_type, category }) {
  return call('create the template', {
    url: `/api/method/${METHOD('create_template')}`,
    method: 'POST',
    params: { title, template_type, category },
  })
}

export function saveTemplateLayout(name, layout, preview_html) {
  return call('save this template', {
    url: `/api/method/${METHOD('save_template_layout')}`,
    method: 'POST',
    params: { name, layout: JSON.stringify(layout), preview_html },
  })
}

export function publishTemplate(name) {
  return call('publish this template', {
    url: `/api/method/${METHOD('publish_template')}`,
    method: 'POST',
    params: { name },
  })
}

export function duplicateTemplate(name, title) {
  return call('duplicate this template', {
    url: `/api/method/${METHOD('duplicate_template')}`,
    method: 'POST',
    params: { name, title },
  })
}

export function createVersion(name, version_label) {
  return call('save a version', {
    url: `/api/method/${METHOD('create_version')}`,
    method: 'POST',
    params: { name, version_label },
  })
}
