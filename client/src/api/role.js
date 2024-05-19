import request from '@/utils/request'

export function getRoutes() {
  return request({
    url: '/abp/manager/api/system/permission/',
    method: 'get'
  })
}

export function getRoleAll() {
  return request({
    url: '/abp/manager/api/system/role/',
    method: 'get'
  })
}

export function createRole(data) {
  return request({
    url: '/abp/manager/api/system/role/',
    method: 'post',
    data
  })
}

export function updateRole(id, data) {
  return request({
    url: `/abp/manager/api/system/role/${id}/`,
    method: 'put',
    data
  })
}

export function deleteRole(id) {
  return request({
    url: `/abp/manager/api/system/role/${id}/`,
    method: 'delete'
  })
}
