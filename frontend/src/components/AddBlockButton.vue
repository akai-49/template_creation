<template>
  <div class="relative flex items-center justify-center py-1">
    <button
      type="button"
      class="z-10 flex h-6 w-6 items-center justify-center rounded-full bg-blue-600 text-white shadow hover:bg-blue-700"
      aria-label="Add block"
      :aria-expanded="open"
      @click="open = !open"
    >
      +
    </button>

    <template v-if="open">
      <div class="fixed inset-0 z-10" @click="open = false" />
      <div
        class="absolute top-7 z-20 grid w-64 grid-cols-4 gap-2 rounded border bg-white p-3 shadow-lg"
      >
        <button
          v-for="lib in library"
          :key="lib.name"
          type="button"
          class="flex flex-col items-center justify-center gap-1 rounded border border-gray-200 p-2 text-[10px] text-gray-600 hover:border-gray-400 hover:bg-gray-50"
          @click="choose(lib)"
        >
          <FeatherIcon :name="lib.icon || 'square'" class="h-4 w-4" />
          {{ lib.block_name }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({ library: { type: Array, default: () => [] } })
const emit = defineEmits(['insert'])

const open = ref(false)
function choose(lib) {
  emit('insert', lib)
  open.value = false
}
</script>
