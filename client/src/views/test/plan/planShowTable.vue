<template>
  <div class="table-wrapper" style="width: auto; height: calc(100vh - 130px)">
    <div class="plan-table-container">
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
            <a @click="copy(scope.row.id)">{{ scope.$index+1 }}</a>
          </template>
        </el-table-column>
        <el-table-column label="计划名称">
          <template slot-scope="scope">
            <a @click="copy(scope.row.name)">{{ scope.row.name }}</a>
          </template>
        </el-table-column>
        <el-table-column label="分组" align="center">
          <template slot-scope="scope">
            <span>{{ groupData[scope.row.group] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="计划类型" width="100" align="center">
          <template slot-scope="scope">
            <span>{{ typeData[scope.row.type] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="创建者" width="100" align="center">
          <template slot-scope="scope">
            <span>{{ userData[scope.row.create_by] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="170" align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.create_time }}</span>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作" width="150">
          <template slot-scope="scope">
            <el-row>
              <el-tooltip
                popper-class="cell-popover"
                trigger="hover"
                placement="top"
                content="修改计划"
              >
                <el-button
                  class="op-btn"
                  icon="el-icon-edit"
                  style="margin-left: 8px"
                  type="text"
                  @click="editPlan(scope.row)"
                />
              </el-tooltip>
              <el-tooltip
                popper-class="cell-popover"
                trigger="hover"
                placement="top"
                content="创建任务"
              >
                <el-button
                  type="text"
                  icon="el-icon-s-promotion"
                  style="margin-left: 8px"
                  @click="createTask(scope.row)"
                />
              </el-tooltip>
              <el-tooltip
                popper-class="cell-popover"
                trigger="hover"
                placement="top"
                content="删除计划"
              >
                <el-button
                  type="text"
                  icon="el-icon-delete"
                  style="margin-left: 8px"
                  @click="deletePlan(scope.row)"
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
import { planDelete, taskPublish } from '@/api/test'

export default {
  name: 'PlanShowTable',
  methods: {
    copy,
    deletePlan(row) {
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          const response = await planDelete(row.id)
          if (response.code === 204) {
            this.$message({
              type: 'success',
              message: '计划删除成功'
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
            message: '已取消删除'
          })
        })
    },
    editPlan(row) {
      this.$store.commit('test/CREATE_PLAN_TYPE', '修改计划')
      this.$store.commit('test/RESET_PLAN_FORM', row)
      this.$store.commit('test/SET_ACTIVE', 2)
      return this.$store.commit('test/CREATE_PLAN_VISIBLE', true)
    },
    createTask(row) {
      this.$confirm('确认执行?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          const response = await taskPublish(row.id)
          if (response.code === 201) {
            this.$message({
              type: 'success',
              message: '任务创建成功'
            })
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
            message: '已取消删除'
          })
        })
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
    }
  }
}

</script>

<style scoped>

</style>
