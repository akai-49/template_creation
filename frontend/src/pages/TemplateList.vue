<template>
  <div class="flex h-full flex-col bg-gray-50">
    <header class="flex items-center justify-between border-b bg-white px-6 py-4">
      <h1 class="text-xl font-semibold text-gray-900">Marketing Studio</h1>
      <Button variant="solid" @click="showNewDialog = true">New Template</Button>
    </header>

    <div class="flex items-center gap-2 border-b bg-white px-6 py-3">
      <button
        v-for="filter in typeFilters"
        :key="filter"
        class="rounded-full px-3 py-1 text-sm"
        :class="
          activeType === filter
            ? 'bg-gray-900 text-white'
            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
        "
        @click="activeType = filter"
      >
        {{ filter }}
      </button>
    </div>

    <div class="flex-1 overflow-y-auto p-6">
      <div v-if="loading" class="text-sm text-gray-500">Loading templates…</div>
      <div
        v-else-if="!templates.length"
        class="flex h-full flex-col items-center justify-center text-gray-400"
      >
        <p>No templates yet. Create your first one.</p>
      </div>
      <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div
          v-for="tpl in filteredTemplates"
          :key="tpl.name"
          class="cursor-pointer rounded-lg border bg-white p-4 shadow-sm transition hover:shadow-md"
          @click="openTemplate(tpl.name)"
        >
          <div
            class="mb-3 flex h-32 items-center justify-center rounded bg-gray-100 text-gray-300"
          >
            <img
              v-if="tpl.thumbnail"
              :src="tpl.thumbnail"
              class="h-full w-full rounded object-cover"
            />
            <span v-else class="text-xs">No preview</span>
          </div>
          <div class="flex items-start justify-between">
            <div>
              <p class="truncate font-medium text-gray-900">{{ tpl.title }}</p>
              <p class="text-xs text-gray-500">{{ tpl.template_type }}</p>
            </div>
            <Badge :variant="tpl.status === 'Published' ? 'solid' : 'subtle'">
              {{ tpl.status }}
            </Badge>
          </div>
        </div>
      </div>
    </div>

    <Dialog v-model="showNewDialog" :options="{ title: 'New Template' }">
      <template #body-content>
        <div class="space-y-4">
          <FormControl
            label="Title"
            v-model="newTemplate.title"
            placeholder="Spring Sale Email"
          />
          <div>
            <label class="mb-1 block text-sm text-gray-600">Template Type</label>
            <select
              v-model="newTemplate.template_type"
              class="w-full rounded border-gray-300 text-sm"
            >
              <option v-for="t in templateTypes" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>
          <Button
            variant="solid"
            class="w-full"
            :disabled="!newTemplate.title"
            @click="handleCreate"
          >
            Create
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { listTemplates, createTemplate } from '../data/api'

const router = useRouter()

const templateTypes = ['Email', 'Web Form', 'Landing Page', 'SMS', 'Popup']
const typeFilters = ['All', ...templateTypes]

const templates = ref([])
const loading = ref(true)
const activeType = ref('All')
const showNewDialog = ref(false)
const newTemplate = ref({ title: '', template_type: 'Email' })

const filteredTemplates = computed(() => {
  if (activeType.value === 'All') return templates.value
  return templates.value.filter((t) => t.template_type === activeType.value)
})

async function fetchTemplates() {
  loading.value = true
  templates.value = await listTemplates()
  loading.value = false
}

async function handleCreate() {
  const name = await createTemplate(newTemplate.value)
  showNewDialog.value = false
  router.push({ name: 'TemplateEditor', params: { name } })
}

function openTemplate(name) {
  router.push({ name: 'TemplateEditor', params: { name } })
}

onMounted(fetchTemplates)
</script>
