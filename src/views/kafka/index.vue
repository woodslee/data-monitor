<template>
  <el-container>
    <el-header style="text-align: right; font-size: 12px">
      <el-select v-model="value" placeholder="Kafka选择">
        <el-option
          v-for="item in kafka_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>
      <el-input v-model="offset" placeholder="offset(timestamp)" />
    </el-header>
    <el-main>
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
    </el-main>
  </el-container>
</template>
<style>
  .el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }
</style>
<script>
import { get_kafka_data } from '@/api/mrs'
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
      kafka_list: [
        {
          label: 'online',
          value: 'online'
        }, {
          label: 'stg',
          value: 'stg'
        }, {
          label: 'data',
          value: 'data'
        }
      ],
      offset: 0
    }
  },
  created() {
    // this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      get_kafka_data().then(response => {
        this.list = response.data.items
        this.listLoading = false
      })
    },
    formatTime,
    parseTime
  }
}
</script>
