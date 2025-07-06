<template>
  <form @submit.prevent="handleSubmit">
    <div class="grid grid-cols-1 grid-rows-8 gap-2 py-5 md:max-w-screen-2xl sd:max-w-screen-sm">
      <div class="row-span-2 text-center md:text-2xl sd:text-xl font-mono">
        <label for="message" class="bg-gradient-to-r from-blue-200 via-blue-400 to-blue-500 inline-block text-transparent bg-clip-text">Check in the Hall of Shame</label>
      </div>
      <div class="row-span-2 py-2">
        <input
            id="message"
            v-model="message"
            type="text"
            maxlength="256"
            class="bg-slate-500 border border-gray-300 text-gray-500 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="For example: kingjames"
            required
        />
      </div>
      <div class="row-span-2 text-center py-2 md:text-lg sd:text-base">
        <button
            type="submit"
            class="submit-button bg-blue-500 hover:bg-blue-700 text-slate-300 font-bold py-2 px-4 rounded-full"
            :disabled="loading">
          {{ loading ? 'Sending...' : 'Submit' }}
        </button>
      </div>
    </div>

    <div v-if="responseText" class="response-box">
      <strong>Server response:</strong>
      <pre>{{ JSON.stringify(responseText) }}</pre>
    </div>

  </form>
</template>

<script setup>

const message = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref(false)
let responseText = ref('')
let apiKey = 'API_KEY' in process.env ? process.env.API_KEY : 'TEST'

const handleSubmit = async () => {
  loading.value = true
  success.value = false
  error.value = false



  try {
    responseText.value = await fetch('/api/v1/scan/username/' + message.value.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        "X-API-KEY": apiKey
      },
      body: JSON.stringify({message: message.value})
    }).then(response => response.json())
    success.value = true
    message.value = ''
  } catch (err) {
    error.value = true
  } finally {
    loading.value = false
  }
}
</script>