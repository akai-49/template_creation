import './index.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

import {
  FrappeUI,
  Button,
  Input,
  TextInput,
  FormControl,
  ErrorMessage,
  Dialog,
  Alert,
  Badge,
  setConfig,
  frappeRequest,
  FeatherIcon,
} from 'frappe-ui'

let globalComponents = {
  Button,
  TextInput,
  Input,
  FormControl,
  ErrorMessage,
  Dialog,
  Alert,
  Badge,
  FeatherIcon,
}

let pinia = createPinia()
let app = createApp(App)

setConfig('resourceFetcher', frappeRequest)
app.use(FrappeUI, { socketio: false })
app.use(pinia)
app.use(router)
for (let key in globalComponents) {
  app.component(key, globalComponents[key])
}

if (import.meta.env.DEV) {
  frappeRequest({
    url: '/api/method/marketing_studio.www.marketing_studio.get_context_for_dev',
  }).then((values) => {
    for (let key in values) {
      window[key] = values[key]
    }
    app.mount('#app')
  })
} else {
  app.mount('#app')
}
