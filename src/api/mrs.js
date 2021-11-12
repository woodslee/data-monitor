import request from '@/utils/request'
export function flink_jobs(params) {
  return request({
    url: '/vue-admin-template/flink/job/list',
    method: 'get',
    params
  })
}
