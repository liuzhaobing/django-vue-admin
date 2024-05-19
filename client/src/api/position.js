import request from '@/utils/request'

export function getPositionAll() {
  return request({
    url: '/abp/manager/api/system/position/',
    method: 'get'
  })
}

export function createPosition(data) {
  return request({
    url: '/abp/manager/api/system/position/',
    method: 'post',
    data
  })
}

export function updatePosition(id, data) {
  return request({
    url: `/abp/manager/api/system/position/${id}/`,
    method: 'put',
    data
  })
}

export function deletePosition(id) {
  return request({
    url: `/abp/manager/api/system/position/${id}/`,
    method: 'delete'
  })
}
