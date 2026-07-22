<template>
  <div class="mb-4">
    <label class="mb-1 block text-xs font-medium text-gray-600">{{ field.label }}</label>

    <textarea
      v-if="field.control === 'textarea'"
      class="w-full rounded border border-gray-300 p-2 text-sm"
      :class="field.monospace ? 'font-mono' : ''"
      rows="4"
      :value="modelValue"
      @change="emitUpdate($event.target.value)"
    />

    <input
      v-else-if="field.control === 'text'"
      class="w-full rounded border border-gray-300 p-2 text-sm"
      :value="modelValue"
      @change="emitUpdate($event.target.value)"
    />

    <div v-else-if="field.control === 'color'" class="flex items-center gap-2">
      <input
        type="color"
        class="h-8 w-10 shrink-0 cursor-pointer rounded border border-gray-300 p-0"
        :value="normalizeHex(modelValue)"
        @input="emitUpdate($event.target.value)"
      />
      <span class="text-xs text-gray-500">{{ modelValue || 'None' }}</span>
      <button
        v-if="modelValue"
        type="button"
        class="ml-auto text-xs text-gray-400 hover:text-gray-600"
        @click="emitUpdate('')"
      >
        Clear
      </button>
    </div>

    <select
      v-else-if="field.control === 'select'"
      class="w-full rounded border border-gray-300 p-2 text-sm"
      :value="modelValue"
      @change="emitUpdate($event.target.value)"
    >
      <option v-for="opt in field.options" :key="opt" :value="opt">{{ opt }}</option>
    </select>

    <div v-else-if="field.control === 'segmented'" class="flex overflow-hidden rounded border border-gray-300">
      <button
        v-for="opt in field.options"
        :key="opt.value"
        type="button"
        class="flex-1 px-2 py-1.5 text-xs transition"
        :class="
          modelValue === opt.value
            ? 'bg-gray-900 text-white'
            : 'bg-white text-gray-600 hover:bg-gray-50'
        "
        @click="emitUpdate(opt.value)"
      >
        {{ opt.label }}
      </button>
    </div>

    <div v-else-if="field.control === 'slider'" class="flex items-center gap-2">
      <input
        type="range"
        class="flex-1"
        :min="field.min"
        :max="field.max"
        :value="modelValue ?? field.min"
        @input="emitUpdate(Number($event.target.value))"
      />
      <span class="w-12 shrink-0 text-right text-xs text-gray-500">
        {{ modelValue ?? field.min }}{{ field.unit }}
      </span>
    </div>

    <label v-else-if="field.control === 'toggle'" class="inline-flex items-center gap-2">
      <input
        type="checkbox"
        :checked="modelValue"
        @change="emitUpdate($event.target.checked)"
      />
      <span class="text-xs text-gray-500">{{ modelValue ? 'Yes' : 'No' }}</span>
    </label>

    <div v-else-if="field.control === 'image'" class="space-y-2">
      <input
        class="w-full rounded border border-gray-300 p-2 text-sm"
        placeholder="Image URL"
        :value="modelValue"
        @change="emitUpdate($event.target.value)"
      />
      <label
        class="inline-flex cursor-pointer items-center gap-2 rounded border border-gray-300 px-2 py-1.5 text-xs text-gray-600 hover:bg-gray-50"
      >
        <input type="file" accept="image/*" class="hidden" @change="handleUpload" />
        {{ isUploading ? `Uploading… ${progress}%` : 'Upload from computer' }}
      </label>
      <p v-if="error" class="text-xs text-red-500">{{ error.message || error }}</p>
    </div>
  </div>
</template>

<script setup>
import { useFileUpload } from 'frappe-ui'

defineProps({
  field: { type: Object, required: true },
  modelValue: { type: [String, Number, Boolean], default: undefined },
})

const emit = defineEmits(['update:modelValue'])

const { upload, isUploading, progress, error } = useFileUpload()

function emitUpdate(value) {
  emit('update:modelValue', value)
}

async function handleUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  try {
    const result = await upload(file, { private: false })
    emitUpdate(result.file_url)
  } catch {
    // error state already surfaced via useFileUpload's `error` ref
  }
  e.target.value = ''
}

function normalizeHex(value) {
  if (/^#[0-9a-fA-F]{6}$/.test(value)) return value
  if (/^#[0-9a-fA-F]{3}$/.test(value)) {
    return (
      '#' +
      value
        .slice(1)
        .split('')
        .map((c) => c + c)
        .join('')
    )
  }
  return '#000000'
}
</script>
