<template>
  <div class="flex gap-3 text-xs text-gray-500" :style="{ padding: paddingStyle(p) }">
    <span v-for="network in activeNetworks" :key="network">{{ network }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const NETWORKS = ['facebook', 'twitter', 'instagram', 'linkedin']

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
const activeNetworks = computed(() => NETWORKS.filter((n) => p.value[n]))
</script>
