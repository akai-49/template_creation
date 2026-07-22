<template>
  <p
    :style="{
      padding: paddingStyle(p),
      fontSize: (p.fontSize ?? 16) + 'px',
      fontWeight: p.fontWeight || 'normal',
      textAlign: p.align || 'left',
      color: p.color || '#111111',
      backgroundColor: p.backgroundColor || undefined,
      whiteSpace: 'pre-wrap',
    }"
  >
    {{ p.text }}
  </p>
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
</script>
