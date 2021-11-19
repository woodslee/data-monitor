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
    url: '/vue-admin-template/kafka/get_data',
    method: 'POST',
    data: params
  })
}

export function get_kafka_list() {
  return request({
    url: '/vue-admin-template/config/kafka_list',
    method: 'GET'
  })
}

export function get_kafka_topic(params) {
  return request({
    url: '/vue-admin-template/kafka/topic',
    method: 'GET',
    params
  })
}

