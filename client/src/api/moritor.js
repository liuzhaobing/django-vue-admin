import { getToken } from '@/utils/auth'
import request from '@/utils/request'

// 查看日志列表

export function getlogList(query) {
  return request({
    url: '/abp/manager/api/monitor/log/',
    method: 'get',
    params: query
  })
}
// 查看日志详情
export function getLog(name) {
  return request({
    url: `/abp/manager/api/monitor/log/${name}/`,
    method: 'get'
  })
}
// 获取服务器状态信息
export function getServerList() {
  return request({
    url: '/abp/manager/api/monitor/server/',
    method: 'get'
  })
}
