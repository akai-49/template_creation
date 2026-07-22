<template>
  <div class="flex h-full flex-col">
    <header class="flex items-center justify-between border-b bg-white px-4 py-3">
      <div class="flex items-center gap-3">
        <Button variant="ghost" @click="$router.push({ name: 'TemplateList' })">
          &larr; Back
        </Button>
        <div v-if="template">
          <p class="text-sm font-semibold text-gray-900">{{ template.title }}</p>
          <p class="text-xs text-gray-500">{{ template.template_type }}</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <div class="flex overflow-hidden rounded border border-gray-300">
          <button
            type="button"
            class="px-2 py-1.5 text-xs"
            :class="previewWidth === 600 ? 'bg-gray-900 text-white' : 'bg-white text-gray-500'"
            @click="previewWidth = 600"
          >
            Desktop
          </button>
          <button
            type="button"
            class="px-2 py-1.5 text-xs"
            :class="previewWidth === 375 ? 'bg-gray-900 text-white' : 'bg-white text-gray-500'"
            @click="previewWidth = 375"
          >
            Mobile
          </button>
        </div>
        <span v-if="saving" class="text-xs text-gray-400">Saving…</span>
        <span v-else-if="lastSaved" class="text-xs text-gray-400">Saved</span>
        <Button @click="showPreview = true">Preview</Button>
        <Button @click="save">Save</Button>
        <Button variant="solid" @click="publish">Publish</Button>
      </div>
    </header>

    <div v-if="!loading" class="flex flex-1 overflow-hidden">
      <div class="flex-1 overflow-y-auto p-6" :style="{ backgroundColor: doc.root.data.backdropColor }">
        <Canvas
          :doc="doc"
          :selected-id="selectedId"
          :library="blockLibrary"
          :width="previewWidth"
          @select="(id) => (selectedId = id)"
          @remove="removeBlock"
          @insert="insertBlockAt"
          @group="groupBlockWithNext"
        />
      </div>

      <Inspector :block="selectedBlock" :doc="doc" @update="updateBlockProp" />
    </div>
    <div v-else class="flex flex-1 items-center justify-center text-sm text-gray-400">
      Loading editor…
    </div>

    <div
      v-if="showPreview"
      class="fixed inset-0 z-20 flex items-center justify-center bg-black/40 p-8"
      @click.self="showPreview = false"
    >
      <div class="flex h-full w-full max-w-3xl flex-col rounded bg-white shadow-xl">
        <div class="flex items-center justify-between border-b px-4 py-2">
          <p class="text-sm font-medium text-gray-700">Email HTML Preview</p>
          <Button variant="ghost" @click="showPreview = false">Close</Button>
        </div>
        <iframe class="flex-1" :srcdoc="previewHtml" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Canvas from '../components/Canvas.vue'
import Inspector from '../components/Inspector.vue'
import {
  createEmptyDocument,
  migrateLegacyLayout,
  deleteBlockDeep,
  insertBlock,
  findParentId,
  groupWithNext,
} from '../data/blockFactory'
import { renderDocumentToHtml } from '../email/renderHtml'
import {
  getBlockLibrary,
  getTemplate,
  saveTemplateLayout,
  publishTemplate,
} from '../data/api'

const route = useRoute()

const loading = ref(true)
const saving = ref(false)
const lastSaved = ref(false)
const showPreview = ref(false)
const previewWidth = ref(600)
const template = ref(null)
const blockLibrary = ref([])
const doc = reactive(createEmptyDocument())
const selectedId = ref(null)

const selectedBlock = computed(() => {
  if (!selectedId.value || !doc[selectedId.value]) return null
  return { id: selectedId.value, ...doc[selectedId.value] }
})

const previewHtml = computed(() => renderDocumentToHtml(doc))

function updateBlockProp({ id, key, value }) {
  const node = doc[id]
  if (node) node.data.props[key] = value
}

function insertBlockAt({ parentId, libraryBlock, index }) {
  const id = insertBlock(doc, parentId, libraryBlock, index)
  selectedId.value = id
}

function removeBlock(id) {
  const parentId = findParentId(doc, id)
  if (parentId) {
    const parentNode = parentId === 'root' ? doc.root : doc[parentId]
    parentNode.data.childrenIds = parentNode.data.childrenIds.filter((c) => c !== id)
  }
  deleteBlockDeep(doc, id)
  if (selectedId.value === id) selectedId.value = null
}

function groupBlockWithNext(id) {
  const columnsId = groupWithNext(doc, id)
  if (columnsId) selectedId.value = columnsId
}

function replaceDoc(newDoc) {
  for (const key of Object.keys(doc)) delete doc[key]
  Object.assign(doc, newDoc)
}

async function loadEditor() {
  loading.value = true
  blockLibrary.value = await getBlockLibrary()

  if (route.params.name) {
    template.value = await getTemplate(route.params.name)
    replaceDoc(migrateLegacyLayout(template.value.layout))
  }
  loading.value = false
}

async function save() {
  if (!template.value) return
  saving.value = true
  await saveTemplateLayout(template.value.name, doc, renderDocumentToHtml(doc))
  saving.value = false
  lastSaved.value = true
}

async function publish() {
  if (!template.value) return
  await save()
  await publishTemplate(template.value.name)
  template.value.status = 'Published'
}

onMounted(loadEditor)
</script>
