<template>
  <div class="card">
    <h3>Entrenamiento del modelo</h3>

    <input type="file" @change="onFileChange" />
    <button @click="train" :disabled="!file || loading">
      Entrenar modelo
    </button>

    <p v-if="loading">Entrenando modelo...</p>

    <div v-if="columns.length">
        <h4> Seleccionar variables</h4>

        <label>X (independiente)</label>
        <select v-model="xCol">
            <option disabled value="">Seleccione</option>
            <option v-for="col in columns" :key="col">
                {{ col }}
            </option>
        </select>

        <label>Y (dependiente)</label>
        <select v-model="yCol">
            <option disabled value="">Seleccione</option>
            <option v-for="col in columns" :key="col">
            {{ col }}
            </option>
        </select>
    </div>

    <div v-if="result">

        <h3>Métricas</h3>
        <p v-if="result.features">
        Variable independiente (X): <strong>{{ result.features.x }}</strong><br>
        Variable dependiente (Y): <strong>{{ result.features.y }}</strong>
        </p>
        <p v-if="result.metrics && result.metrics.train">R² (Entrenamiento): {{ result.metrics.train.r2_score ? result.metrics.train.r2_score.toFixed(4) : 'N/A' }}</p>
        <p v-if="result.metrics && result.metrics.test">R² (Prueba): {{ result.metrics.test.r2_score ? result.metrics.test.r2_score.toFixed(4) : 'N/A' }}</p>
        <p v-if="result.metrics && result.metrics.test">RMSE (Prueba): {{ result.metrics.test.rmse ? result.metrics.test.rmse.toFixed(4) : 'N/A' }}</p>

        <h3 v-if="result.train">Entrenamiento</h3>
        <RegressionChart
            v-if="result.train"
            :x="result.train.x"
            :yReal="result.train.y_real"
            :yPred="result.train.y_pred"
        />

        <h3 v-if="result.test">Prueba</h3>
        <RegressionChart
            v-if="result.test"
            :x="result.test.x"
            :yReal="result.test.y_real"
            :yPred="result.test.y_pred"
        />
    </div>

    <div v-if="result && result.warnings && result.warnings.correlation">
        <div :class="['warning', result.warnings.correlation.level]">
            {{ result.warnings.correlation.message }}
            <br v-if="result.warnings.correlation.correlation" />
            <span v-if="result.warnings.correlation.correlation">
              Correlación: {{ result.warnings.correlation.correlation.toFixed(3) }}
            </span>
        </div>

        <div v-if="result.warnings.fitting" class="warning fit">
            {{ result.warnings.fitting.message }}
        </div>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { trainModel, getColumns } from '../services/api'
import RegressionChart from './RegressionChart.vue'

const emit = defineEmits(['trained'])

const file = ref(null)
const columns = ref([])
const xCol = ref('')
const yCol = ref('')

const result = ref(null)
const loading = ref(false)
const error = ref(null)
const warning = ref(null)

async function onFileChange(e) {
  file.value = e.target.files[0]
  result.value = null
  warning.value = null
  error.value = null

  if (!file.value) return

  try {
    const response = await getColumns(file.value)
    columns.value = response.numeric_columns || []
  } catch (err) {
    error.value = 'No se pudieron obtener las columnas'
  }
}

watch([xCol, yCol], () => {
  warning.value = null
})

async function train() {
  if (!file.value) {
    error.value = 'Debe cargar un archivo'
    return
  }

  if (!xCol.value || !yCol.value) {
    error.value = 'Debe seleccionar columnas X e Y'
    return
  }

  if (xCol.value === yCol.value) {
    error.value = 'X e Y deben ser diferentes'
    return
  }

  loading.value = true
  error.value = null
  warning.value = null

  try {
    result.value = await trainModel(
      file.value,
      xCol.value,
      yCol.value
    )

    // Advertencia por bajo R²
    if (result.value.metrics?.r2 < 0.3) {
      warning.value =
        'Advertencia: correlación baja. El modelo podría no ser adecuado para estos datos.'
    }

    emit('trained', true)
  } catch (err) {
    error.value = err.message || 'Error al entrenar el modelo'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.card {
  padding: 1rem;
  border: 1px solid #ccc;
  margin-bottom: 1rem;
}
.error {
  color: red;
}
.warning {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  color: black;
}

.warning.low {
  background-color: #ffe0e0;
}

.warning.medium {
  background-color: #fff3cd;
}

.warning.high {
  background-color: #e0ffe0;
}

.warning.fit {
  background-color: #e0f0ff;
}
</style>
