<template>
  <div class="app-container">
    <div style="display: flex;justify-content: flex-end;padding-bottom:10px">
      <el-select v-model="cur_kafka" placeholder="请选择Kafka集群" style="margin-right:10px" @change="onSelectedKfaka">
        <el-option
          v-for="item in kafka_list"
          :key="item.name"
          :label="item.name"
          :value="item.name"
        />
      </el-select>
      <el-select v-model="cur_topic" filterable="true" placeholder="请选择Topic" style="margin-right:10px">
        <el-option
          v-for="item in topic_list"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>
      <el-select v-model="cur_model" style="margin-right:10px;width:100px">
        <el-option
          v-for="item in models"
          :key="item.name"
          :label="item.name"
          :value="item.value"
        />
      </el-select>
      <el-select v-model="cur_decoder" style="margin-right:10px;width:100px">
        <el-option
          v-for="item in decoders"
          :key="item.value"
          :label="item.name"
          :value="item.value"
        />
      </el-select>
      <el-input
        v-model="offset"
        placeholder="输入offset"
        clearable
        style="width: 100px;margin-right: 10px"
      />
      <el-button icon="el-icon-search" type="primary" @click="fetchData">
        搜索
      </el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="序号" width="50">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="APP_ID" width="250">
        <template slot-scope="scope">
          {{ scope.row.id }}
        </template>
      </el-table-column>
      <el-table-column label="名称">
        <template slot-scope="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="类型" width="110" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.applicationType }}</span>
        </template>
      </el-table-column>
      <el-table-column label="开始时间" width="140" align="center">
        <template slot-scope="scope">
          {{ parseTime(scope.row.startedTime) }}
        </template>
      </el-table-column>
      <el-table-column label="结束时间" width="130" align="center">
        <template slot-scope="scope">
          {{ scope.row.finishedTime==0?'-':formatTime(scope.row.finishedTime) }}
        </template>
      </el-table-column>
      <el-table-column label="运行时长" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.elapsedTime }}
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { get_kafka_list, get_kafka_topic, get_kafka_data } from '@/api/mrs'
import { formatTime, parseTime } from '@/utils/index'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      list: null,
      listLoading: false,
      cur_kafka: '',
      cur_topic: '',
      cur_model: 1,
      cur_decoder: 'TBox',
      kafka_list: this.getKafkaList(),
      topic_list: [],
      offset: 0,
      models: [{ name: 'ME7', value: 0 }, { name: 'ME5', value: 1 }],
      decoders: [{ name: 'Tbox', value: 'TBox' }, { name: '其他', value: 'Decoder' }]
    }
  },
  created() {
    // this.fetchData()
    this.kafka_list = this.getKafkaList()
  },
  methods: {
    fetchData() {
      if (this.cur_topic === '') return
      this.listLoading = true
      get_kafka_data({
        broker: this.cur_kafka,
        topic: this.cur_topic,
        offset: this.offset,
        model: this.cur_model,
        decoder: this.cur_decoder
      }).then(response => {
        this.list = response.data.items
        this.listLoading = false
      })
    },
    getKafkaList() {
      get_kafka_list().then(response => {
        this.kafka_list = response.data
      })
    },
    onSelectedKfaka(item) {
      get_kafka_topic({ broker: item }).then(response => {
        this.topic_list = response.data
      })
    },
    formatTime,
    parseTime
  }
}
</script>
