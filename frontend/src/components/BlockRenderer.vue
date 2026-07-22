<template>
  <div
    class="ms-canvas-block group relative rounded"
    :class="{ 'is-selected': selectedId === block.id }"
    :style="wrapperStyle"
    @click.stop="$emit('select', block.id)"
  >
    <template v-if="selectedId === block.id">
      <div class="absolute -top-3 right-1 z-10 flex gap-1">
        <button
          class="rounded bg-gray-700 px-1.5 py-0.5 text-[10px] text-white shadow"
          title="Place next block beside this one"
          @click.stop="$emit('group', block.id)"
        >
          ⇄ Columns
        </button>
        <button
          class="rounded bg-red-500 px-1.5 py-0.5 text-[10px] text-white shadow"
          @click.stop="$emit('remove', block.id)"
        >
          Delete
        </button>
      </div>

      <!-- ponytail: width handles move widthPercent, top/bottom handles move padding; separate from Image's own content-width slider, unify if it confuses people -->
      <div
        v-if="!isContainer"
        class="absolute -right-1.5 top-1/2 z-10 h-8 w-3 -translate-y-1/2 cursor-ew-resize rounded bg-blue-500 shadow"
        @mousedown.stop="(e) => startResize(e, 'right')"
      />
      <div
        v-if="!isContainer"
        class="absolute -left-1.5 top-1/2 z-10 h-8 w-3 -translate-y-1/2 cursor-ew-resize rounded bg-blue-500 shadow"
        @mousedown.stop="(e) => startResize(e, 'left')"
      />
      <div
        class="absolute -top-1.5 left-1/2 z-10 h-3 w-8 -translate-x-1/2 cursor-ns-resize rounded bg-blue-500 shadow"
        @mousedown.stop="(e) => startResize(e, 'top')"
      />
      <div
        class="absolute -bottom-1.5 left-1/2 z-10 h-3 w-8 -translate-x-1/2 cursor-ns-resize rounded bg-blue-500 shadow"
        @mousedown.stop="(e) => startResize(e, 'bottom')"
      />
    </template>

    <component
      :is="blockComponent"
      :block="block"
      :doc="doc"
      :selected-id="selectedId"
      :library="library"
      @select="(id) => $emit('select', id)"
      @remove="(id) => $emit('remove', id)"
      @insert="(payload) => $emit('insert', payload)"
      @group="(id) => $emit('group', id)"
    />
  </div>
</template>

<script setup>
import { computed, onUnmounted } from 'vue'
import SectionBlock from './blocks/SectionBlock.vue'
import ColumnsBlock from './blocks/ColumnsBlock.vue'
import HeaderBlock from './blocks/HeaderBlock.vue'
import FooterBlock from './blocks/FooterBlock.vue'
import TextBlock from './blocks/TextBlock.vue'
import ButtonBlock from './blocks/ButtonBlock.vue'
import ImageBlock from './blocks/ImageBlock.vue'
import VideoBlock from './blocks/VideoBlock.vue'
import DividerBlock from './blocks/DividerBlock.vue'
import SpacerBlock from './blocks/SpacerBlock.vue'
import SocialIconsBlock from './blocks/SocialIconsBlock.vue'
import FormFieldBlock from './blocks/FormFieldBlock.vue'
import HtmlBlock from './blocks/HtmlBlock.vue'

const props = defineProps({
  block: { type: Object, required: true },
  doc: { type: Object, required: true },
  selectedId: { type: String, default: null },
  library: { type: Array, default: () => [] },
})
defineEmits(['select', 'remove', 'insert', 'group'])

const REGISTRY = {
  Section: SectionBlock,
  Columns: ColumnsBlock,
  Header: HeaderBlock,
  Footer: FooterBlock,
  Text: TextBlock,
  Button: ButtonBlock,
  Image: ImageBlock,
  Video: VideoBlock,
  Divider: DividerBlock,
  Spacer: SpacerBlock,
  'Social Icons': SocialIconsBlock,
  'Form Field': FormFieldBlock,
  HTML: HtmlBlock,
}
const CONTAINER_TYPES = new Set(['Section', 'Columns', 'Header', 'Footer'])

const blockComponent = computed(() => REGISTRY[props.block.type] || TextBlock)
const isContainer = computed(() => CONTAINER_TYPES.has(props.block.type))

const wrapperStyle = computed(() => {
  const w = props.block.data.props?.widthPercent
  if (!w || w >= 100) return {}
  const align = props.block.data.props?.align || 'left'
  const margin =
    align === 'center'
      ? { marginLeft: 'auto', marginRight: 'auto' }
      : align === 'right'
        ? { marginLeft: 'auto' }
        : { marginRight: 'auto' }
  return { width: w + '%', ...margin }
})

let dragState = null
function startResize(e, edge) {
  const el = e.currentTarget.parentElement
  const rect = el.getBoundingClientRect()
  const parentWidth = el.parentElement.getBoundingClientRect().width
  const p = props.block.data.props
  dragState = {
    edge,
    startX: e.clientX,
    startY: e.clientY,
    startWidth: rect.width,
    parentWidth,
    startPaddingTop: p.paddingTop ?? 0,
    startPaddingBottom: p.paddingBottom ?? 0,
  }
  window.addEventListener('mousemove', onResize)
  window.addEventListener('mouseup', stopResize)
}
function onResize(e) {
  if (!dragState) return
  const p = props.block.data.props
  if (dragState.edge === 'right' || dragState.edge === 'left') {
    const dx = dragState.edge === 'right' ? e.clientX - dragState.startX : dragState.startX - e.clientX
    const newWidthPx = dragState.startWidth + dx
    p.widthPercent = Math.min(100, Math.max(10, Math.round((newWidthPx / dragState.parentWidth) * 100)))
  } else if (dragState.edge === 'top') {
    const dy = dragState.startY - e.clientY
    p.paddingTop = Math.min(80, Math.max(0, Math.round(dragState.startPaddingTop + dy)))
  } else if (dragState.edge === 'bottom') {
    const dy = e.clientY - dragState.startY
    p.paddingBottom = Math.min(80, Math.max(0, Math.round(dragState.startPaddingBottom + dy)))
  }
}
function stopResize() {
  dragState = null
  window.removeEventListener('mousemove', onResize)
  window.removeEventListener('mouseup', stopResize)
}
onUnmounted(stopResize)
</script>
