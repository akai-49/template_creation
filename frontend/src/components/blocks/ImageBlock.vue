<template>
  <div :style="{ padding: paddingStyle(p), textAlign: p.align || 'center' }">
    <div
      v-if="!p.src"
      class="inline-flex items-center justify-center rounded bg-gray-100 text-xs text-gray-400"
      :style="{ width: (p.width ?? 100) + '%', minHeight: '80px' }"
    >
      Image placeholder
    </div>
    <img
      v-else
      :src="p.src"
      :alt="p.alt"
      :style="{ width: (p.width ?? 100) + '%', maxWidth: '100%', display: 'inline-block' }"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
</script>
