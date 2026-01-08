<template>
  <div class="card">
    <h3>Predicción</h3>

    <label>Variable X (separadas por coma)</label>
    <input v-model="input" placeholder="Ej: 9, 10, 11, 12" />

    <button @click="makePrediction" :disabled="loading || !values.length">
      Predecir
    </button>

    <div v-if="predictions && predictions.length > 0">
      <h4>Resultados</h4>
      <ul>
        <li v-for="(p, i) in predictions" :key="i">
          Valor {{ values[i] }} → {{ p.toFixed(2) }}
        </li>
      </ul>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { predict } from '../services/api'

const input = ref('')
const predictions = ref([])
const loading = ref(false)
const error = ref(null)

const values = computed(() =>
  input.value
    .split(',')
    .map(v => Number(v.trim()))
    .filter(v => !isNaN(v))
)

async function makePrediction() {
  loading.value = true
  error.value = null
  predictions.value = []

  try {
    const res = await predict(values.value)
    predictions.value = res.predictions || []
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.card {
  padding: 1rem;
  border: 1px solid #ccc;
}
.error {
  color: red;
}
</style>
