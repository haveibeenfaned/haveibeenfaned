<template>
  <div class="form-container">
    <form @submit.prevent="handleSubmit" class="form-box">
      <label for="message" class="form-label">Check in the Hall of Shame</label>
      <input
          id="message"
          v-model="message"
          type="text"
          maxlength="256"
          class="form-input"
          placeholder="Enter your message"
          required
      />
      <button
          type="submit"
          class="submit-button"
          :disabled="loading"
      >
        {{ loading ? 'Sending...' : 'Submit' }}
      </button>

      <p v-if="success" class="success-message">Message sent successfully!</p>
      <p v-if="error" class="error-message">Error sending message.</p>

      <div v-if="responseText" class="response-box">
        <strong>Server response:</strong>
        <pre>{{ responseText }}</pre>
      </div>

    </form>
  </div>
</template>

<script setup>

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
    responseText.value = await fetch('/api/v1/scan/username/' + message.value.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
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