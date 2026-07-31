<template>
  <FrappeUIProvider>
    <div class="h-full">
      <div
        v-if="fatalError"
        role="alert"
        class="flex h-full flex-col items-center justify-center gap-3 p-8 text-center"
      >
        <h1 class="text-lg font-semibold text-gray-900">Something broke in the builder</h1>
        <p class="max-w-md text-sm text-gray-500">{{ fatalError }}</p>
        <Button variant="solid" @click="reload">Reload</Button>
      </div>
      <router-view v-else />
    </div>
  </FrappeUIProvider>
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { FrappeUIProvider } from 'frappe-ui'

const fatalError = ref(null)

// Error boundary: a render or lifecycle error anywhere below shows this fallback
// instead of leaving the user staring at a blank canvas.
onErrorCaptured((error) => {
  fatalError.value = error?.message || String(error)
  console.error(error)
  return false
})

function reload() {
  window.location.reload()
}
</script>
