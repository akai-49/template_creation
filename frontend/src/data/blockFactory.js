const CONTAINER_TYPES = new Set(['Section', 'Columns', 'Header', 'Footer'])

export function isContainer(blockType) {
  return CONTAINER_TYPES.has(blockType)
}

export function createBlockId() {
  return 'blk_' + Math.random().toString(36).slice(2, 10)
}

export const DOCUMENT_STYLE_DEFAULTS = {
  backdropColor: '#f4f4f5',
  canvasColor: '#ffffff',
  canvasBorderColor: '',
  canvasBorderRadius: 0,
  fontFamily: 'Modern sans',
  textColor: '#111111',
}

/**
 * Document shape (flat map, inspired by usewaypoint/email-builder-js):
 * {
 *   root: { type: 'EmailLayout', data: { childrenIds: ['blk_a', 'blk_b'], ...DOCUMENT_STYLE_DEFAULTS } },
 *   blk_a: { type: 'Text', data: { props: {...} } },
 *   blk_b: { type: 'Columns', data: { props: {...}, childrenIds: ['blk_c'] } },
 *   blk_c: { type: 'Text', data: { props: {...} } },
 * }
 */
export function createEmptyDocument() {
  return {
    root: { type: 'EmailLayout', data: { childrenIds: [], ...DOCUMENT_STYLE_DEFAULTS } },
  }
}

/** Fills in any missing document-level style fields (used after load, for docs saved before they existed). */
export function normalizeDocument(doc) {
  doc.root.data = { ...DOCUMENT_STYLE_DEFAULTS, ...doc.root.data }
  return doc
}

export function instantiateBlock(libraryBlock) {
  const node = {
    id: createBlockId(),
    type: libraryBlock.block_type,
    block_name: libraryBlock.block_name,
    data: { props: { ...(libraryBlock.default_props || {}) } },
  }
  if (isContainer(libraryBlock.block_type)) {
    node.data.childrenIds = []
  }
  return node
}

/** Inserts a new block (from the library) into parentId's children at `index` (end if omitted). */
export function insertBlock(doc, parentId, libraryBlock, index) {
  const node = instantiateBlock(libraryBlock)
  doc[node.id] = { type: node.type, block_name: node.block_name, data: node.data }
  const parentNode = parentId === 'root' ? doc.root : doc[parentId]
  const ids = parentNode.data.childrenIds || (parentNode.data.childrenIds = [])
  const at = index === undefined ? ids.length : index
  ids.splice(at, 0, node.id)
  return node.id
}

export function paddingStyle(props = {}) {
  const t = props.paddingTop ?? 0
  const r = props.paddingRight ?? 0
  const b = props.paddingBottom ?? 0
  const l = props.paddingLeft ?? 0
  return `${t}px ${r}px ${b}px ${l}px`
}

/** Finds the parentId (or 'root') whose childrenIds contains `id`. */
export function findParentId(doc, id) {
  if ((doc.root.data.childrenIds || []).includes(id)) return 'root'
  for (const key of Object.keys(doc)) {
    if (key === 'root') continue
    if ((doc[key].data.childrenIds || []).includes(id)) return key
  }
  return null
}

/** Wraps `id` and its next sibling into a new Columns block, so they sit side by side. */
export function groupWithNext(doc, id) {
  const parentId = findParentId(doc, id)
  if (!parentId) return null
  const parentNode = parentId === 'root' ? doc.root : doc[parentId]
  const ids = parentNode.data.childrenIds
  const index = ids.indexOf(id)
  const nextId = ids[index + 1]
  if (!nextId) return null

  const columnsId = createBlockId()
  doc[columnsId] = {
    type: 'Columns',
    block_name: 'Columns',
    data: { props: { backgroundColor: '', gap: 16 }, childrenIds: [id, nextId] },
  }
  ids.splice(index, 2, columnsId)
  return columnsId
}

export function getChildrenIds(doc, parentId) {
  const node = parentId === 'root' ? doc.root : doc[parentId]
  return node?.data?.childrenIds || []
}

export function deleteBlockDeep(doc, id) {
  const node = doc[id]
  if (!node) return
  const childIds = node.data?.childrenIds || []
  for (const childId of childIds) {
    deleteBlockDeep(doc, childId)
  }
  delete doc[id]
}

/**
 * Convert the old nested {blocks:[{id,block_type,props,children:[]}]} layout
 * (used before the flat-map refactor) into the current document shape.
 */
export function migrateLegacyLayout(layout) {
  if (!layout || layout.root) return normalizeDocument(layout || createEmptyDocument())
  if (!Array.isArray(layout.blocks)) return createEmptyDocument()

  const doc = { root: { type: 'EmailLayout', data: { childrenIds: [] } } }

  function addBlock(legacyBlock) {
    const id = legacyBlock.id || createBlockId()
    const node = {
      type: legacyBlock.block_type,
      block_name: legacyBlock.block_name,
      data: { props: { ...(legacyBlock.props || {}) } },
    }
    if (Array.isArray(legacyBlock.children)) {
      node.data.childrenIds = legacyBlock.children.map(addBlock)
    }
    doc[id] = node
    return id
  }

  doc.root.data.childrenIds = layout.blocks.map(addBlock)
  return normalizeDocument(doc)
}
