import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

export async function getColumns(file) {
  const formData = new FormData()
  formData.append('file', file)

  const res = await api.post('/columns', formData)
  return res.data
}

export async function trainModel(file, xCol, yCol) {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('x_col', xCol)
  formData.append('y_col', yCol)

  const res = await api.post('/train', formData)
  return res.data
}

export async function predict(values) {
  const res = await api.post('/predict', { x: values })
  return res.data
}