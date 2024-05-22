<template>
  <div class="app-container">
    <task-filter-bar
      :group-list="groupList.results"
      :type-list="typeList.results"
      :user-list="userList"
      :list-query.sync="listQuery"
      @refresh="getTaskList"
    />
    <task-show-table
      :data="dataList.results"
      :group-data="groupData"
      :type-data="typeData"
      :user-data="userData"
      :status-data="statusData"
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
import { arrayToMap } from '@/utils/common'
import { groupList, taskList, typeList, statusList } from '@/api/test'

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
  computed: {
    statusData() {
      if (this.statusList.count >= 0) {
        return arrayToMap(this.statusList.results, 'id', 'name')
      }
    },
    groupData() {
      if (this.groupList.count >= 0) {
        return arrayToMap(this.groupList.results, 'id', 'name')
      }
    },
    typeData() {
      if (this.typeList.count >= 0) {
        return arrayToMap(this.typeList.results, 'id', 'name')
      }
    },
    userList() {
      return this.$store.state.user.users
    },
    userData() {
      return this.$store.state.user.usersIdName
    }
  },
  created() {
    this.getStatusList()
    this.getGroupList()
    this.getTypeList()
    this.getTaskList()
  },
  methods: {
    getStatusList() {
      statusList({ page: 1, page_size: 100 }).then(response => {
        if (response.data) {
          this.statusList = response.data
        }
      })
    },
    getGroupList() {
      groupList({ page: 1, page_size: 100 }).then(response => {
        if (response.data) {
          this.groupList = response.data
        }
      })
    },
    getTypeList() {
      typeList({ page: 1, page_size: 100 }).then(response => {
        if (response.data) {
          this.typeList = response.data
        }
      })
    },
    getTaskList() {
      this.listLoading = true
      taskList(this.listQuery).then(response => {
        if (response.data) {
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
