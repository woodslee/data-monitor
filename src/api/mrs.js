import request from '@/utils/request'
export function flink_jobs(params) {
  return request({
    url: '/vue-admin-template/flink/job/list',
    method: 'get',
    params
  })
}

export function get_kafka_data(params) {
  return request({
    url: '/vue-admin-template/kafka/list_data',
    method: 'POST',
    params
  })
}
