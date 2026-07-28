import api from './api'

export function createResourceService(endpoint) {
  return {
    getAll() {
      return api.get(`${endpoint}/`)
    },
    getById(id) {
      return api.get(`${endpoint}/${id}/`)
    },
    create(data) {
      return api.post(`${endpoint}/`, data)
    },
    update(id, data) {
      return api.put(`${endpoint}/${id}/`, data)
    },
    patch(id, data) {
      return api.patch(`${endpoint}/${id}/`, data)
    },
    delete(id) {
      return api.delete(`${endpoint}/${id}/`)
    }
  }
}