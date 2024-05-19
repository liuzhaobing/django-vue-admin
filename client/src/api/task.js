import request from '@/utils/request'

export function getptaskList(query) {
  return request({
    url: '/abp/manager/api/system/ptask/',
    method: 'get',
    params: query
  })
}

export function getTaskAll() {
  return request({
    url: '/abp/manager/api/system/task/',
    method: 'get'
  })
}
export function createptask(data) {
  return request({
    url: '/abp/manager/api/system/ptask/',
    method: 'post',
    data
  })
}

export function updateptask(id, data) {
  return request({
    url: `/abp/manager/api/system/ptask/${id}/`,
    method: 'put',
    data
  })
}

export function toggletask(id) {
  return request({
    url: `/abp/manager/api/system/ptask/${id}/toggle/`,
    method: 'put'
  })
}

export function deleteptask(id) {
  return request({
    url: `/abp/manager/api/system/ptask/${id}/`,
    method: 'delete'
  })
}
