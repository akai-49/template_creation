<template>
  <div class="min-h-[48px] p-3" :style="containerStyle">
    <p class="mb-1 text-[10px] font-medium uppercase text-gray-400">{{ block.block_name }}</p>
    <ContainerChildren
      :doc="doc"
      :parent-id="block.id"
      :selected-id="selectedId"
      :library="library"
      direction="row"
      @select="(id) => $emit('select', id)"
      @remove="(id) => $emit('remove', id)"
      @insert="(p) => $emit('insert', p)"
      @group="(id) => $emit('group', id)"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ContainerChildren from '../ContainerChildren.vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({
  block: { type: Object, required: true },
  doc: { type: Object, required: true },
  selectedId: { type: String, default: null },
  library: { type: Array, default: () => [] },
})
defineEmits(['select', 'remove', 'insert', 'group'])

const containerStyle = computed(() => ({
  backgroundColor: props.block.data.props?.backgroundColor,
  gap: (props.block.data.props?.gap ?? 16) + 'px',
  padding: paddingStyle(props.block.data.props),
}))
</script>
