import { computed } from 'vue'

/**
 * Bridges the flat block-map document to vuedraggable's array-based v-model.
 * `doc` is a reactive flat map ({ root, [id]: node }); `parentId` is 'root'
 * or a container block's id. The returned computed's getter resolves
 * childrenIds into concrete block objects; the setter writes new/reordered
 * ids back into the parent's childrenIds and registers any newly-cloned
 * blocks (dragged in from the palette) into the flat map.
 */
export function useChildrenModel(doc, parentId) {
  return computed({
    get() {
      const node = parentId === 'root' ? doc.root : doc[parentId]
      const ids = node?.data?.childrenIds || []
      return ids.filter((id) => doc[id]).map((id) => ({ id, ...doc[id] }))
    },
    set(newList) {
      const node = parentId === 'root' ? doc.root : doc[parentId]
      if (!node) return
      for (const item of newList) {
        if (!doc[item.id]) {
          doc[item.id] = {
            type: item.type,
            block_name: item.block_name,
            data: item.data,
          }
        }
      }
      node.data.childrenIds = newList.map((item) => item.id)
    },
  })
}
