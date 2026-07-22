<template>
  <div class="space-y-1" :style="{ padding: paddingStyle(p) }">
    <label class="text-xs font-medium text-gray-600">
      {{ p.label }}<span v-if="p.required" class="text-red-500">*</span>
    </label>
    <input
      class="w-full rounded border border-gray-300 px-2 py-1 text-sm"
      :placeholder="p.placeholder"
      disabled
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { paddingStyle } from '../../data/blockFactory'

const props = defineProps({ block: { type: Object, required: true } })
const p = computed(() => props.block.data.props || {})
</script>
