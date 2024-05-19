import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/abp/manager/api/token/',
    method: 'post',
    data
  })
}

export function logout() {
  return request({
    url: '/abp/manager/api/token/black/',
    method: 'get'
  })
}

export function getInfo() {
  return request({
    url: '/abp/manager/api/system/user/info/',
    method: 'get'
  })
}

export function getUserList(query) {
  return request({
    url: '/abp/manager/api/system/user/',
    method: 'get',
    params: query
  })
}

export function getUser(id) {
  return request({
    url: `/abp/manager/api/system/user/${id}/`,
    method: 'get'
  })
}

export function createUser(data) {
  return request({
    url: '/abp/manager/api/system/user/',
    method: 'post',
    data
  })
}

export function updateUser(id, data) {
  return request({
    url: `/abp/manager/api/system/user/${id}/`,
    method: 'put',
    data
  })
}

export function deleteUser(id, data) {
  return request({
    url: `/abp/manager/api/system/user/${id}/`,
    method: 'delete',
    data
  })
}

export function changePassword(data) {
  return request({
    url: '/abp/manager/api/system/user/password/',
    method: 'put',
    data
  })
}
