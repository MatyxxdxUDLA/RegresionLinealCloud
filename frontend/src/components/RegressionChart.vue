
<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue'
import { Chart } from 'chart.js/auto'

const props = defineProps({
  x: Array,
  yReal: Array,
  yPred: Array
})

const chartCanvas = ref(null)
let chartInstance = null

// Plugin para redibujar la línea al final
const regressionOnTopPlugin = {
  id: 'regressionOnTop',
  afterDatasetsDraw(chart, args, pluginOptions) {
    // Localiza el dataset de la línea por su etiqueta (ajústalo si cambias el label)
    const dsIndex = chart.data.datasets.findIndex(d => d.label === 'Línea de regresión')
    if (dsIndex === -1) return

    const ds = chart.data.datasets[dsIndex]
    const meta = chart.getDatasetMeta(dsIndex)
    const ctx = chart.ctx

    // Si el dataset está oculto, no dibujar
    if (!meta || meta.hidden) return

    // Traza la línea encima de todo (usando las posiciones ya calculadas)
    ctx.save()
    ctx.lineWidth = ds.borderWidth ?? 3
    ctx.strokeStyle = ds.borderColor ?? 'rgba(255, 99, 132, 1)'
    ctx.setLineDash(ds.borderDash ?? [])
    ctx.lineJoin = 'round'
    ctx.lineCap = 'round'

    ctx.beginPath()
    meta.data.forEach((el, i) => {
      const { x, y } = el.getProps(['x', 'y'], true)
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    ctx.stroke()
    ctx.restore()
  }
}

function renderChart() {
  if (chartInstance) chartInstance.destroy()

  chartInstance = new Chart(chartCanvas.value, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Datos reales',
          type: 'scatter',
          order: 0,
          data: props.x.map((val, i) => ({ x: val, y: props.yReal[i] })),
          pointRadius: 3,
          pointBackgroundColor: 'rgba(75, 192, 192, 0.8)',
          pointBorderColor: 'rgba(75, 192, 192, 1)',
          pointBorderWidth: 1,
          showLine: false
        },
        {
          label: 'Línea de regresión',
          type: 'line',
          order: 1, // el orden ya no importa, el plugin dibuja encima
          data: props.x.map((val, i) => ({ x: val, y: props.yPred[i] })),
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 3,
          fill: false,
          pointRadius: 0,
          tension: 0.1
        }
      ]
    },
    options: {
      responsive: true,
      animation: false,
      plugins: {
        legend: {
          labels: {
            // opcional: asegura que el orden visual del legend sea el que quieras
            // sort: (a, b) => a.text === 'Datos reales' ? -1 : 1
          }
        }
      },
      scales: {
        x: { title: { display: true, text: 'Variable X' }},
        y: { title: { display: true, text: 'Variable Y' }}
      }
    },
    plugins: [regressionOnTopPlugin]
  })
}

watch(() => [props.x, props.yReal, props.yPred], renderChart, { deep: true })
onMounted(renderChart)
</script>