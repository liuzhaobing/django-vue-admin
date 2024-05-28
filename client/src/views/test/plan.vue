<template>
  <div class="app-container">
    <plan-filter-bar
      :list-query.sync="listQuery"
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
import { planList } from '@/api/test'
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
  created() {
    this.getPlanList()
  },
  methods: {
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
