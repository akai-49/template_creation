<template>
  <draggable
    v-model="children"
    :group="{ name: 'blocks' }"
    item-key="id"
    class="flex min-h-[32px] gap-2"
    :class="direction === 'row' ? 'flex-row' : 'flex-col'"
  >
    <template #item="{ element }">
      <BlockRenderer
        :block="element"
        :doc="doc"
        :selected-id="selectedId"
        :library="library"
        :class="direction === 'row' ? 'flex-1' : ''"
        @select="(id) => $emit('select', id)"
        @remove="(id) => $emit('remove', id)"
        @insert="(payload) => $emit('insert', payload)"
        @group="(id) => $emit('group', id)"
      />
    </template>
  </draggable>
  <div class="pt-1" @click.stop>
    <AddBlockButton
      :library="library"
      @insert="(lib) => $emit('insert', { parentId, libraryBlock: lib })"
    />
  </div>
</template>

<script setup>
import draggable from 'vuedraggable'
import BlockRenderer from './BlockRenderer.vue'
import AddBlockButton from './AddBlockButton.vue'
import { useChildrenModel } from '../composables/useChildrenModel'

const props = defineProps({
  doc: { type: Object, required: true },
  parentId: { type: String, required: true },
  selectedId: { type: String, default: null },
  library: { type: Array, default: () => [] },
  direction: { type: String, default: 'col' },
})
defineEmits(['select', 'remove', 'insert', 'group'])

const children = useChildrenModel(props.doc, props.parentId)
</script>
