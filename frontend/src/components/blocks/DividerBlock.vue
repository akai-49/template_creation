<template>
  <div :style="{ padding: paddingStyle(p) }">
    <hr
      :style="{
        borderColor: p.color || '#e5e7eb',
        borderTopWidth: (p.thickness ?? 1) + 'px',
      }"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
</script>
