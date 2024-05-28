<template>
  <div class="app-container">
    <plan-filter-bar
      :list-query.sync="listQuery"
      :group-list="groupList.results"
      :type-list="typeList.results"
      :user-list="userList"
      @refresh="getPlanList"
    />
    <plan-show-table
      :data="dataList.results"
      @refresh="getPlanList"
    />
    <pagination
      v-show="dataList.count>0"
      :total="dataList.count"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size"
      @pagination="getPlanList"
    />
    <plan-add-dialog />
  </div>
</template>

<script>
import PlanShowTable from '@/views/test/plan/planShowTable.vue'
import PlanAddDialog from '@/views/test/plan/planAddDialog.vue'
import Pagination from '@/components/Pagination/index.vue'
import { planList, groupList, typeList } from '@/api/test'
import { arrayToMap } from '@/utils/common'
import PlanFilterBar from '@/views/test/plan/planFilterBar.vue'

export default {
  name: 'Plan',
  components: { PlanFilterBar, Pagination, PlanShowTable, PlanAddDialog },
  data() {
    return {
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
    this.getGroupList()
    this.getTypeList()
    this.getPlanList()
  },
  methods: {
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
    getPlanList() {
      this.listLoading = true
      planList(this.listQuery).then(response => {
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
      this.getPlanList()
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getPlanList()
    }
  }
}
</script>

<style scoped>

</style>
