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
        height="calc(100vh - 130px)"
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
            <span>{{ scope.row.type_name }}</span>
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
            <span>{{ scope.row.status_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="执行者" width="100" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.create_user }}</span>
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
              <el-popover
                width="300"
                trigger="click"
                title="文件下载"
              >
                <div>
                  <p>选择下载测试结果或者测试用例</p>
                  <el-button
                    v-show="scope.row.result_file"
                    size="mini"
                    type="success"
                    @click="handleMissionDownload(scope.row, 1)"
                  >
                    测试结果
                  </el-button>
                  <el-button
                    v-show="scope.row.case_file"
                    size="mini"
                    type="primary"
                    @click="handleMissionDownload(scope.row, 0)"
                  >
                    测试用例
                  </el-button>
                </div>
                <el-button
                  slot="reference"
                  type="text"
                  icon="el-icon-download"
                />
              </el-popover>
              <el-tooltip
                v-show="hasPermission(['task_continue'])"
                popper-class="cell-popover"
                trigger="hover"
                placement="top"
                content="重启任务"
              >
                <el-button
                  type="text"
                  icon="el-icon-s-promotion"
                  style="margin-left: 8px"
                  @click="rerunTask(scope.row)"
                />
              </el-tooltip>
              <el-tooltip
                v-show="hasPermission(['task_stop'])"
                popper-class="cell-popover"
                trigger="hover"
                placement="top"
                content="停止任务"
              >
                <el-button
                  type="text"
                  icon="el-icon-switch-button"
                  style="margin-left: 8px"
                  @click="stopTask(scope.row)"
                  :disabled="scope.row.status !== 256 && scope.row.status !== 512"
                />
              </el-tooltip>
              <el-tooltip
                v-show="hasPermission(['task_delete'])"
                popper-class="cell-popover"
                trigger="hover"
                placement="top"
                content="删除任务"
              >
                <el-button
                  type="text"
                  icon="el-icon-delete"
                  style="margin-left: 8px"
                  @click="deleteTask(scope.row)"
                />
              </el-tooltip>
            </el-row>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { copy } from '@/utils/common'
import { taskDelete, taskDeletion, taskContinue, taskStop } from '@/api/test'
import { Message } from 'element-ui'
import { hasPermission } from '@/permission'

export default {
  name: 'TaskShowTable',
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    data: {
      required: true,
      type: Array,
      default: () => []
    }
  },
  methods: {
    hasPermission,
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
    stopTask(row) {
      this.$confirm('确认停止?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async() => {
          const response = await taskStop(row.job_instance_id)
          if (response.code === 201) {
            this.$message({
              type: 'success',
              message: '任务停止成功'
            })
            this.$emit('refresh')
          } else {
            this.$message({
              type: 'error',
              message: response.msg
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    rerunTask(row) {
      this.$confirm('确认继续?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async() => {
          const response = await taskContinue(row.job_instance_id)
          if (response.code === 200) {
            this.$message({
              type: 'success',
              message: '任务继续成功'
            })
            this.$emit('refresh')
          } else {
            this.$message({
              type: 'error',
              message: response.msg
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    handleMissionDownload(row, type) {
      try {
        const a = document.createElement('a')
        a.href = type === 1 ? `/abp/manager/${row.result_file}` : `/abp/manager/${row.case_file}`
        a.click()
        window.URL.revokeObjectURL(a.href)
        Message.success('下载成功！')
      } catch (error) {
        Message.error('下载失败！')
      }
    },
    deleteTask(row) {
      this.$confirm(`确认删除 ⌜${row.name}⌟ ？`, '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async() => {
          let response
          if (row.id) {
            response = await taskDelete(row.id)
          } else {
            response = await taskDeletion(row.job_instance_id)
          }
          if (response.code === 204) {
            this.$message({
              type: 'success',
              message: '任务删除成功'
            })
            this.$emit('refresh')
          } else {
            this.$message({
              type: 'error',
              message: response.msg
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    }
  }
}

</script>

<style scoped>

</style>
