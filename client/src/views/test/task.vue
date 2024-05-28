<template>
  <div class="app-container">
    <task-filter-bar
      :list-query.sync="listQuery"
      @refresh="getTaskList"
    />
    <task-show-table
      :data="dataList.results"
      @refresh="getTaskList"
    />
    <pagination
      v-show="dataList.count>0"
      :total="dataList.count"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size"
      @pagination="getTaskList"
    />
  </div>
</template>

<script>

import TaskFilterBar from '@/views/test/task/taskFilterBar.vue'
import TaskShowTable from '@/views/test/task/taskShowTable.vue'
import Pagination from '@/components/Pagination/index.vue'
import { taskList, taskRunningList } from '@/api/test'

export default {
  components: { Pagination, TaskFilterBar, TaskShowTable },
  data() {
    return {
      statusList: { count: 0 },
      groupList: { count: 0 },
      typeList: { count: 0 },
      dataList: { count: 0 },
      listLoading: true,
      listQuery: {
        page: 1,
        page_size: 20
      }
    }
  },
  created() {
    this.getTaskList()
  },
  methods: {
    async getTaskList() {
      this.listLoading = true
      let data = []
      if (this.listQuery.page === 1) {
        await taskRunningList(this.listQuery).then(response => {
          if (response.data) {
            data = response.data.results
          }
        })
      }
      await taskList(this.listQuery).then(response => {
        if (response.data) {
          data = [...data, ...response.data.results]
          response.data.results = data
          this.dataList = response.data
        }
        this.listLoading = false
      })
    },
    resetFilter() {
      this.listQuery = {
        page: 1,
        page_size: 20
      }
      this.getTaskList()
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getTaskList()
    }
  }
}

</script>

<style scoped>

</style>
