<template>
  <div :style="{ height: (p.height ?? 24) + 'px', padding: paddingStyle(p) }" />
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
</script>
