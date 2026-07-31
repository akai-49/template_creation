<template>
  <div
    class="rounded border border-dashed border-gray-300 text-xs text-gray-400"
    :style="{ padding: paddingStyle(p) }"
  >
    Custom HTML block
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
</script>
