import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'TemplateList',
    component: () => import('./pages/TemplateList.vue'),
  },
  {
    path: '/template/new',
    name: 'NewTemplate',
    component: () => import('./pages/TemplateEditor.vue'),
  },
  {
    path: '/template/:name',
    name: 'TemplateEditor',
    component: () => import('./pages/TemplateEditor.vue'),
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory('/marketing-studio'),
  routes,
})

export default router
