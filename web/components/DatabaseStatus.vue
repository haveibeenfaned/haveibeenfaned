<template>
  <div v-if="crawlerStatus" class="response-box">
    <strong>Crawler Status response:</strong>
    <pre>{{ crawlerStatus }}</pre>
  </div>
  <div v-if="databaseStatus" class="response-box">
    <strong>Database Status response:</strong>
    <pre>{{ databaseStatus }}</pre>
  </div>
</template>

<script setup lang="ts">

const message = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(false)
let crawlerStatus = ref('')
let databaseStatus = ref('')

const handleStatus = async () => {
  loading.value = true
  success.value = false
  error.value = false

  try {
    crawlerStatus.value = await fetch('/api/v1/crawler/status/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({message: message.value})
    }).then(response => response.json()).then(response => response[0][0].join(":"))
    success.value = true
    message.value = ''
  } catch (err) {
    error.value = true
  } finally {
    loading.value = false
  }

  try {
    databaseStatus.value = await fetch('/api/v1/database/status/' + message.value.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({message: message.value})
    }).then(response => response.json()).then(response => response[0][0].join(":"))
    success.value = true
    message.value = ''
  } catch (err) {
    error.value = true
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>

</style>