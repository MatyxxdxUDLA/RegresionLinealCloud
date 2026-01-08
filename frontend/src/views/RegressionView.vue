<template>
  <div class="container">
    <h2>Regresión Lineal – Ventas por Hora</h2>

    <TrainModel @trained="modelReady = true" />

    <PredictModel v-if="modelReady" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TrainModel from '../components/TrainModel.vue'
import PredictModel from '../components/PredictModel.vue'

const modelReady = ref(false)
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
}
</style>
