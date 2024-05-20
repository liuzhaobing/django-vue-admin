import { getToken } from '@/utils/auth'
import request from '@/utils/request'

export function upUrl() {
  return '/abp/manager/api/file/'
}

export function upHeaders() {
  return { Authorization: 'Bearer ' + getToken() }
}

export function getFileList(query) {
  return request({
    url: '/abp/manager/api/file/',
    method: 'get',
    params: query
  })
}

export function deleteFile(_id) {
  return request({
    url: `/abp/manager/api/file/${_id}/`,
    method: 'delete'
  })
}
