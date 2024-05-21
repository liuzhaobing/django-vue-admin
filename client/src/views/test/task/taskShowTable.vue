<template>
  <div class="table-wrapper" style="width: auto; height: calc(100vh - 130px)">
    <div class="task-table-container">
      <el-table
        v-loading="loading"
        :data="data"
        element-loading-text="Loading"
        border
        fit
        width="100%"
        height="calc(100vh - 180px)"
        row-key="id"
        :highlight-current-row="true"
        :row-style="{height: '50px'}"
        :cell-style="{padding: '1px'}"
        :header-cell-style="{
          'background-color': '#F5F7FA',
          color: '#303133',
          padding: '3px'
        }"
      >
        <el-table-column align="center" label="#" width="40">
          <template slot-scope="scope">
            <a @click="copy(scope.row.job_instance_id)">{{ scope.$index+1 }}</a>
          </template>
        </el-table-column>
        <el-table-column label="任务名称">
          <template slot-scope="scope">
            <a @click="copy(scope.row.name)">{{ scope.row.name }}</a>
          </template>
        </el-table-column>
        <el-table-column label="任务类型" width="100" align="center">
          <template slot-scope="scope">
            <span>{{ typeData[scope.row.type] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="执行进度" width="150" align="center">
          <template slot-scope="scope">
            <el-progress :text-inside="true" :stroke-width="16" :percentage="scope.row.progress_percent" :color="showProgressPercentColor(scope.row.progress_percent)" />
          </template>
        </el-table-column>
        <el-table-column label="用例进度" width="120" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.progress }}</span>
          </template>
        </el-table-column>
        <el-table-column label="评测指标" width="100" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.metrics }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80" align="center">
          <template slot-scope="scope">
            <span>{{ statusData[scope.row.status] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="执行者" width="100" align="center">
          <template slot-scope="scope">
            <span>{{ userData[scope.row.create_by] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="开始时间" width="170" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.start_time }}</span>
          </template>
        </el-table-column>
        <el-table-column label="结束时间" width="170" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.end_time }}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作" width="170">
          <template slot-scope="scope">
            <el-row>
            </el-row>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { copy } from '@/utils/common'

export default {
  name: 'TaskShowTable',
  methods: {
    copy,
    showProgressPercentColor(percent) {
      const candidateColors = [
        '#006064',
        '#00838F',
        '#00ACC1',
        '#26C6DA',
        '#80DEEA',
        '#90CAF9',
        '#64B5F6',
        '#42A5F5',
        '#2196F3',
        '#1976D2',
        '#42A5F5'
      ]
      return candidateColors[Math.floor(percent / 10)]
    },
  },
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    data: {
      required: true,
      type: Array,
      default: () => []
    },
    userData: {
      required: true,
      type: Object,
      default: () => {
        return {}
      }
    },
    typeData: {
      required: true,
      type: Object,
      default: () => {
        return {}
      }
    },
    groupData: {
      required: true,
      type: Object,
      default: () => {
        return {}
      }
    },
    statusData: {
      required: true,
      type: Object,
      default: () => {
        return {}
      }
    }
  }
}

</script>

<style scoped>

</style>
