<template>
  <div class="mx-auto min-h-full" :style="canvasStyle" @click="$emit('select', null)">
    <draggable
      v-model="children"
      :group="{ name: 'blocks' }"
      item-key="id"
      class="flex min-h-[100px] flex-col gap-2 p-4"
      ghost-class="opacity-40"
    >
      <template #item="{ element }">
        <BlockRenderer
          :block="element"
          :doc="doc"
          :selected-id="selectedId"
          :library="library"
          @select="(id) => $emit('select', id)"
          @remove="(id) => $emit('remove', id)"
          @insert="(payload) => $emit('insert', payload)"
          @group="(id) => $emit('group', id)"
        />
      </template>
    </draggable>
    <!-- ponytail: append-only insert (top-level) + drag-to-reorder covers insert-at-position; add mid-list "+" when users ask for it -->
    <div class="pb-4" @click.stop>
      <AddBlockButton :library="library" @insert="(lib) => $emit('insert', { parentId: 'root', libraryBlock: lib })" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import draggable from 'vuedraggable'
import BlockRenderer from './BlockRenderer.vue'
import AddBlockButton from './AddBlockButton.vue'
import { useChildrenModel } from '../composables/useChildrenModel'

const props = defineProps({
  doc: { type: Object, required: true },
  selectedId: { type: String, default: null },
  library: { type: Array, default: () => [] },
  width: { type: Number, default: 600 },
})

defineEmits(['select', 'remove', 'insert', 'group'])

const children = useChildrenModel(props.doc, 'root')

const canvasStyle = computed(() => ({
  maxWidth: props.width + 'px',
  backgroundColor: props.doc.root.data.canvasColor || '#ffffff',
  borderColor: props.doc.root.data.canvasBorderColor || undefined,
  borderWidth: props.doc.root.data.canvasBorderColor ? '1px' : undefined,
  borderStyle: props.doc.root.data.canvasBorderColor ? 'solid' : undefined,
  borderRadius: (props.doc.root.data.canvasBorderRadius ?? 0) + 'px',
  color: props.doc.root.data.textColor || undefined,
  fontFamily: FONT_STACKS[props.doc.root.data.fontFamily] || FONT_STACKS['Modern sans'],
}))

const FONT_STACKS = {
  'Modern sans': 'Arial, Helvetica, sans-serif',
  Serif: 'Georgia, "Times New Roman", serif',
  Monospace: '"Courier New", monospace',
}
</script>
