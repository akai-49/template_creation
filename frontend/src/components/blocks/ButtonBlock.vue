<template>
  <div :style="{ padding: paddingStyle(p), textAlign: p.align || 'left' }">
    <a
      :style="{
        display: p.width === 'full' ? 'block' : 'inline-block',
        textAlign: 'center',
        backgroundColor: p.backgroundColor || '#5b21b6',
        color: p.textColor || '#ffffff',
        fontSize: (p.fontSize ?? 16) + 'px',
        fontWeight: p.fontWeight || 'bold',
        borderRadius: styleRadius,
        padding: '10px 20px',
        textDecoration: 'none',
      }"
    >
      {{ p.label }}
    </a>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
const styleRadius = computed(() => {
  if (p.value.style === 'pill') return '999px'
  if (p.value.style === 'rectangle') return '0px'
  return '6px'
})
</script>
