<template>
  <div class="form-box">
    <strong class="form-label">Crawler Status:</strong>
    <div v-if="crawlerStatus === 'False'" class="form-label">
      <pre>{{ 'Crawler is either Stopped / Paused / On Maintenance. Your requests will be processed at a later date!'	}}</pre>
    </div>
    <div v-if="crawlerStatus === 'True'">
      <pre>{{ 'Crawler is Running. Your requests will be processed in real time!'	}}</pre>
    </div>
    <div v-if="databaseStatus === 'False'" class="form-label">
      <strong class="form-label">Database Status: </strong>
      <pre>{{ 'Database is either Stopped / Paused / On Maintenance. Your requests will be processed at a later date!'	}}</pre>
    </div>
    <div v-if="databaseStatus === 'True' && crawlerStatus === 'True'" class="form-label">
      <strong class="form-label">Database Status: </strong>
      <pre>{{ 'Database is Running. Your requests will be stored and processed in real time!'	}}</pre>
    </div>
    <div v-if="databaseStatus === 'True' && crawlerStatus === 'False'" class="form-label">
      <strong class="form-label">Database Status: </strong>
      <pre>{{ 'Database is Running. However the Crawler is not Running. Your Requests will be stored but not processed.'	}}</pre>
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

const handleStatus = async () => {
  loading.value = true
  success.value = false
  error.value = false

  try {
    crawlerStatus.value = await fetch('/api/v1/status/crawler', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
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
        'Content-Type': 'application/json'
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