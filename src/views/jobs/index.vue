<template>

  <div class="app-container">
    <div style="display: flex;justify-content: space-between; padding-bot">
      <div>
        <el-input
          v-model="keyword"
          placeholder="请输入员工名进行搜索，可以直接回车搜索..."
          prefix-icon="el-icon-search"
          clearable
          style="width: 350px;margin-right: 10px"
          :disabled="showAdvanceSearchView"
          @clear="initEmps"
          @keydown.enter.native="initEmps"
        />
        <el-button icon="el-icon-search" type="primary" :disabled="showAdvanceSearchView" @click="initEmps">
          搜索
        </el-button>
        <el-button type="primary" @click="showAdvanceSearchView = !showAdvanceSearchView">
          <i
            :class="showAdvanceSearchView?'fa fa-angle-double-up':'fa fa-angle-double-down'"
            aria-hidden="true"
          />
          高级搜索
        </el-button>
      </div>
      <div>
        <el-upload
          :show-file-list="false"
          :before-upload="beforeUpload"
          :on-success="onSuccess"
          :on-error="onError"
          :disabled="importDataDisabled"
          style="display: inline-flex;margin-right: 8px"
          action="/employee/basic/import"
        >
          <el-button :disabled="importDataDisabled" type="success" :icon="importDataBtnIcon">
            {{ importDataBtnText }}
          </el-button>
        </el-upload>
        <el-button type="success" icon="el-icon-download" @click="exportData">
          导出数据
        </el-button>
        <el-button type="primary" icon="el-icon-plus" @click="showAddEmpView">
          添加用户
        </el-button>
      </div>
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
import { flink_jobs } from '@/api/mrs'
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
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      flink_jobs().then(response => {
        this.list = response.data.items
        this.listLoading = false
      })
    },
    formatTime,
    parseTime
  }
}
</script>
