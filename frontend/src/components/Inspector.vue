<template>
  <div class="flex h-full w-72 flex-col overflow-y-auto border-l bg-white">
    <div class="flex border-b">
      <button
        class="flex-1 border-b-2 px-3 py-2 text-xs font-semibold uppercase tracking-wide"
        :class="activeTab === 'styles' ? 'border-gray-900 text-gray-900' : 'border-transparent text-gray-400'"
        @click="activeTab = 'styles'"
      >
        Styles
      </button>
      <button
        class="flex-1 border-b-2 px-3 py-2 text-xs font-semibold uppercase tracking-wide"
        :class="activeTab === 'inspect' ? 'border-gray-900 text-gray-900' : 'border-transparent text-gray-400'"
        @click="activeTab = 'inspect'"
      >
        Inspect
      </button>
    </div>

    <div v-if="activeTab === 'styles'" class="p-4">
      <p class="mb-3 text-xs font-semibold uppercase tracking-wide text-gray-400">
        {{ DOCUMENT_SCHEMA.label }}
      </p>
      <PropertyField
        v-for="field in DOCUMENT_SCHEMA.fields"
        :key="field.key"
        :field="field"
        :model-value="doc.root.data[field.key]"
        @update:model-value="(v) => (doc.root.data[field.key] = v)"
      />
    </div>

    <div v-else class="p-4">
      <div v-if="!block" class="text-sm text-gray-400">Select a block to edit its properties.</div>
      <div v-else>
        <p class="mb-3 text-sm font-medium text-gray-800">{{ schema.label }}</p>
        <PropertyField
          v-for="field in schema.fields"
          :key="field.key"
          :field="field"
          :model-value="block.data.props[field.key]"
          @update:model-value="(v) => update(field.key, v)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import PropertyField from './PropertyField.vue'
import { BLOCK_SCHEMAS, DOCUMENT_SCHEMA } from '../data/blockSchemas'

const props = defineProps({
  block: { type: Object, default: null },
  doc: { type: Object, required: true },
})

const emit = defineEmits(['update'])

const activeTab = ref('styles')
watch(
  () => props.block,
  (val) => {
    activeTab.value = val ? 'inspect' : 'styles'
  },
)

const schema = computed(() => BLOCK_SCHEMAS[props.block?.type] || { label: 'Block', fields: [] })

function update(key, value) {
  emit('update', { id: props.block.id, key, value })
}
</script>
