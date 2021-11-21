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
      <el-select v-model="cur_topic" filterable placeholder="请选择Topic" style="margin-right:10px">
        <el-option
          v-for="item in topic_list"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>
    </div>
    <div style="display: flex;justify-content: flex-end;padding-bottom:10px">
      <el-input
        v-model="vin"
        placeholder="VIN"
        clearable
        style="width: 150px;margin-right: 10px"
      />
      <el-select v-model="cur_type" style="margin-right:10px">
        <el-option
          v-for="item in type_cmds"
          :key="item.name"
          :label="item.name"
          :value="item.value"
        />
      </el-select>
      <el-select v-model="cur_cmd" placeholder="请选择CMD" style="margin-right:10px">
        <el-option
          v-for="item in cmds"
          :key="item.value"
          :label="`${item.name}(cmd=${item.value})`"
          :value="item.value"
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
      <el-table-column label="PID" width="50">
        <template slot-scope="scope">
          {{ scope.row.partition }}
        </template>
      </el-table-column>
      <el-table-column label="vin" width="160">
        <template slot-scope="scope">
          <span>{{ scope.row.vin }}</span>
        </template>
      </el-table-column>
      <el-table-column label="type" width="50">
        <template slot-scope="scope">
          <span>{{ scope.row.type }}</span>
        </template>
      </el-table-column>
      <el-table-column label="cmd" width="50" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.cmd }}</span>
        </template>
      </el-table-column>
      <el-table-column label="数据时间" width="140" align="center">
        <template slot-scope="scope">
          {{ scope.row.obj.data_time }}
        </template>
      </el-table-column>
      <el-table-column label="上报时间" width="140" align="center">
        <template slot-scope="scope">
          {{ scope.row.report_time }}
        </template>
      </el-table-column>
      <el-table-column label="kafka时间" width="140" align="center">
        <template slot-scope="scope">
          {{ scope.row.received_ts }}
        </template>
      </el-table-column>
      <el-table-column label="秒包" align="center">
        <template slot-scope="scope">
          {{ scope.row.obj.pkg_num }}
        </template>
      </el-table-column>
      <el-table-column label="故障" align="center">
        <template slot-scope="scope">
          {{ scope.row.obj.is_fault }}
        </template>
      </el-table-column>
      <el-table-column label="payload" width="140" align="center">
        <template slot-scope="scope">
          {{ scope.row.data_len }}
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="handleDetail(scope.$index, scope.row)"
          >详情</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { get_kafka_list, get_kafka_topic, get_kafka_data } from '@/api/mrs'
import { formatTime, parseTime } from '@/utils/index'
var type_cmd = [
  { name: '数据上报',
    value: 1,
    cmds: [{
      name: '国标实发',
      value: 1
    }, {
      name: '国标补发',
      value: 2
    }, {
      name: '企标实发',
      value: 3
    }, {
      name: '企标实发',
      value: 4
    }, {
      name: 'MISC',
      value: 7
    }, {
      name: '自检',
      value: 8
    }, {
      name: 'MSD',
      value: 11
    }]
  }, { name: '常规命令',
    value: 4,
    cmds: [{
      name: '登入',
      value: 1
    }, {
      name: '登出',
      value: 2
    }, {
      name: '心跳',
      value: 3
    }] }
]

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
      vin: '',
      type_cmds: type_cmd,
      cur_type: type_cmd[0].value,
      cur_cmd: null,
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
  computed: {
    cmds: function(param) {
      console.info('cur_type: ', this.cur_type)
      for (var i = 0; i < type_cmd.length; i++) {
        if (type_cmd[i].value === this.cur_type) {
          return type_cmd[i].cmds
        }
      }
      return []
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
        this.list = response.data
        this.listLoading = false
      }).catch(function(err) {
        console.info('catched exception:', err)
        console.info(this)
        this.list = []
        this.listLoading = false
      })
    },
    getKafkaList() {
      get_kafka_list().then(response => {
        this.kafka_list = response.data
      }, function(err) {
        console.error(err)
        this.kafka_list = []
      })
    },
    onSelectedKfaka(item) {
      get_kafka_topic({ broker: item }).then(response => {
        this.topic_list = response.data
      }, function(err) {
        console.error(err)
        this.topic_list = []
      })
    },
    handleDetail(index, row) {
      console.info(index, row)
    },
    getCmds(param) {
      console.info('get_cmd:', param)
      return []
    },
    formatTime,
    parseTime
  }
}
</script>
