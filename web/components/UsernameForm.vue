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
    const response = await fetch('/api/v1/scan/username/' + message.value.toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({message: message.value})
    }).then(response => response.json()).then(response => response[0][0].join(":"))
    responseText.value = response
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
.form-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
}

.form-box {
  background-color: transparent; /* Background made transparent */
  border: none;
  padding: 24px;
  border-radius: 8px;
  box-shadow: none;
  display: flex;
  flex-direction: column;
  align-items: center; /* Center child elements horizontally */
}

.form-label {
  font-style: italic;
  font-family: 'Andale Mono', serif;
  font-size: 17px;
  font-weight: 500;
  color: #333;
  text-align: center; /* Center label text */
  margin-bottom: 8px;
  width: 100%;
}

.form-input {
  width: 100%;
  max-width: 100%;
  padding: 10px 12px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  border-color: #007bff;
  outline: none;
}

.submit-button {
  background-color: #007bff;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.submit-button:hover:enabled {
  background-color: #0056b3;
}

.success-message {
  color: green;
  margin-top: 12px;
  font-weight: 500;
}

.error-message {
  color: red;
  margin-top: 10%;
  font-weight: 500;
  font-family: "Andale Mono", sans-serif;
  font-style: italic;
}
</style>
