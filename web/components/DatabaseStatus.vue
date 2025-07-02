<script setup lang="ts">

const message = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(false)
let responseText = ref('')

const handleSubmit = async () => {
  loading.value = true
  success.value = false
  error.value = false

  try {
    responseText.value = await fetch('/api/v1/crawler/status/', {
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
    responseText.value = await fetch('/api/v1/database/status/' + message.value.toString(), {
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

<template>

</template>

<style scoped>

</style>