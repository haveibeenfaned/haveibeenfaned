<template>
  <div class="grid grid-cols-1 grid-rows-2 justify-items-center py-9">
    <div v-if="crawlerStatus === 'False'" class="grid-col-start-1 grid-row-start-2">
      <pre class="text-slate-300">          Crawler 🔴</pre>
      <pre class="text-slate-300">Requests will not be processed</pre>
    </div>
    <div v-if="crawlerStatus === 'True'" class="grid-col-start-1 grid-row-start-2">
      <pre class="text-slate-300">Crawler 🟢</pre>
    </div>
    <div v-if="databaseStatus === 'False'" class="grid-col-start-1 grid-row-start-2">
      <pre class="text-slate-300">Database 🔴</pre>
    </div>
    <div v-if="databaseStatus === 'True' && crawlerStatus === 'True'" class="grid-col-start-1 grid-row-start-1">
      <pre class="text-slate-300">Database 🟢</pre>
    </div>
    <div v-if="databaseStatus === 'True' && crawlerStatus === 'False'" class="grid-col-start-1 grid-row-start-1">
      <pre class="text-slate-300">Database 🟠</pre>
    </div>
  </div>

</template>

<script setup>

const message = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(false)
let crawlerStatus = ref('')
let databaseStatus = ref('')
let apiKey = 'API_KEY' in process.env ? process.env.API_KEY : 'TEST'

const handleStatus = async () => {
  loading.value = true
  success.value = false
  error.value = false

  try {
    crawlerStatus.value = await fetch('/api/v1/status/crawler', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey
      }
    }).then(response => response.json())
    success.value = true
    message.value = ''
  } catch (err) {
    error.value = true
    console.error(err)
  } finally {
    loading.value = false
  }

  try {
    databaseStatus.value = await fetch('/api/v1/status/database' + message.value.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-API-KEY': apiKey
      }
    }).then(response => response.json())
    success.value = true
    message.value = ''
  } catch (err) {
    error.value = true
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => handleStatus())
</script>

<style scoped>

</style>