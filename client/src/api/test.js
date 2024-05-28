import request from '@/utils/request'

export function planCreate(data) {
  return request({
    url: '/abp/manager/api/test/plan/',
    method: 'post',
    data
  })
}

export function planUpdate(data) {
  return request({
    url: `/abp/manager/api/test/plan/${data._id}/`,
    method: 'put',
    data
  })
}

export function planRetrieve(_id) {
  return request({
    url: `/abp/manager/api/test/plan/${_id}/`,
    method: 'get'
  })
}

export function planList(query) {
  return request({
    url: '/abp/manager/api/test/plan/',
    method: 'get',
    params: query
  })
}

export function planDelete(_id) {
  return request({
    url: `/abp/manager/api/test/plan/${_id}/`,
    method: 'delete'
  })
}

export function taskPublish(_id) {
  return request({
    url: `/abp/manager/api/test/plan/${_id}/_publish/`,
    method: 'get'
  })
}

export function taskCreate(data) {
  return request({
    url: '/abp/manager/api/test/task/',
    method: 'post',
    data
  })
}

export function taskUpdate(data) {
  return request({
    url: `/abp/manager/api/test/task/${data._id}/`,
    method: 'put',
    data
  })
}

export function taskRetrieve(_id) {
  return request({
    url: `/abp/manager/api/test/task/${_id}/`,
    method: 'get'
  })
}

export function taskList(query) {
  return request({
    url: '/abp/manager/api/test/task/',
    method: 'get',
    params: query
  })
}

export function taskRunningList(query) {
  return request({
    url: '/abp/manager/api/test/task/_running/',
    method: 'get',
    params: query
  })
}

export function taskDelete(_id) {
  return request({
    url: `/abp/manager/api/test/task/${_id}/`,
    method: 'delete'
  })
}

export function taskDeletion(job_instance_id) {
  return request({
    url: `/abp/manager/api/test/task/${job_instance_id}/_deletion/`,
    method: 'delete'
  })
}

export function taskStop(_id) {
  return request({
    url: `/abp/manager/api/test/task/${_id}/_stop/`,
    method: 'post'
  })
}

export function taskContinue(_id) {
  return request({
    url: `/abp/manager/api/test/task/${_id}/_continue/`,
    method: 'post'
  })
}

export function groupCreate(data) {
  return request({
    url: '/abp/manager/api/test/group/',
    method: 'post',
    data
  })
}

export function groupUpdate(data) {
  return request({
    url: `/abp/manager/api/test/group/${data._id}/`,
    method: 'put',
    data
  })
}

export function groupRetrieve(_id) {
  return request({
    url: `/abp/manager/api/test/group/${_id}/`,
    method: 'get'
  })
}

export function groupList(query) {
  return request({
    url: '/abp/manager/api/test/group/',
    method: 'get',
    params: query
  })
}

export function groupDelete(_id) {
  return request({
    url: `/abp/manager/api/test/group/${_id}/`,
    method: 'delete'
  })
}

export function typeCreate(data) {
  return request({
    url: '/abp/manager/api/test/type/',
    method: 'post',
    data
  })
}

export function typeUpdate(data) {
  return request({
    url: `/abp/manager/api/test/type/${data._id}/`,
    method: 'put',
    data
  })
}

export function typeRetrieve(_id) {
  return request({
    url: `/abp/manager/api/test/type/${_id}/`,
    method: 'get'
  })
}

export function typeList(query) {
  return request({
    url: '/abp/manager/api/test/type/',
    method: 'get',
    params: query
  })
}

export function typeDelete(_id) {
  return request({
    url: `/abp/manager/api/test/type/${_id}/`,
    method: 'delete'
  })
}

export function statusCreate(data) {
  return request({
    url: '/abp/manager/api/test/status/',
    method: 'post',
    data
  })
}

export function statusUpdate(data) {
  return request({
    url: `/abp/manager/api/test/status/${data._id}/`,
    method: 'put',
    data
  })
}

export function statusRetrieve(_id) {
  return request({
    url: `/abp/manager/api/test/status/${_id}/`,
    method: 'get'
  })
}

export function statusList(query) {
  return request({
    url: '/abp/manager/api/test/status/',
    method: 'get',
    params: query
  })
}

export function statusDelete(_id) {
  return request({
    url: `/abp/manager/api/test/status/${_id}/`,
    method: 'delete'
  })
}

export function logCreate(data) {
  return request({
    url: '/abp/manager/api/test/log/',
    method: 'post',
    data
  })
}

export function logUpdate(data) {
  return request({
    url: `/abp/manager/api/test/log/${data._id}/`,
    method: 'put',
    data
  })
}

export function logRetrieve(_id) {
  return request({
    url: `/abp/manager/api/test/log/${_id}/`,
    method: 'get'
  })
}

export function logList(query) {
  return request({
    url: '/abp/manager/api/test/log/',
    method: 'get',
    params: query
  })
}

export function logDelete(_id) {
  return request({
    url: `/abp/manager/api/test/log/${_id}/`,
    method: 'delete'
  })
}

export function reportCreate(data) {
  return request({
    url: '/abp/manager/api/test/report/',
    method: 'post',
    data
  })
}

export function reportUpdate(data) {
  return request({
    url: `/abp/manager/api/test/report/${data._id}/`,
    method: 'put',
    data
  })
}

export function reportRetrieve(_id) {
  return request({
    url: `/abp/manager/api/test/report/${_id}/`,
    method: 'get'
  })
}

export function reportList(query) {
  return request({
    url: '/abp/manager/api/test/report/',
    method: 'get',
    params: query
  })
}

export function reportDelete(_id) {
  return request({
    url: `/abp/manager/api/test/report/${_id}/`,
    method: 'delete'
  })
}
