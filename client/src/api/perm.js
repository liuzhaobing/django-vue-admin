import request from '@/utils/request'

export function getPermAll() {
  return request({
    url: '/abp/manager/api/system/permission/',
    method: 'get'
  })
}
export function createPerm(data) {
  return request({
    url: '/abp/manager/api/system/permission/',
    method: 'post',
    data
  })
}
export function updatePerm(id, data) {
  return request({
    url: `/abp/manager/api/system/permission/${id}/`,
    method: 'put',
    data
  })
}
export function deletePerm(id) {
  return request({
    url: `/abp/manager/api/system/permission/${id}/`,
    method: 'delete'
  })
}
