<template>
  <div :style="{ padding: paddingStyle(p) }">
    <div class="flex h-32 items-center justify-center rounded bg-gray-900 text-xs text-white">
      {{ p.url || 'Video placeholder' }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
</script>
