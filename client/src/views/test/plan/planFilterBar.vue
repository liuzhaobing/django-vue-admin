<template>
  <div class="filter-container">
    <el-autocomplete
      v-model="listQuery.name"
      :fetch-suggestions="nameFilterAsync"
      placeholder="名称搜索"
      size="mini"
      style="width: 350px;"
      @select="handleFilter"
    >
      <i slot="suffix" class="el-input__icon el-icon-search" @click="handleFilter" />
    </el-autocomplete>
    <el-button type="primary" icon="el-icon-refresh" size="mini" @click="handleFilter">刷新</el-button>
    <el-button type="primary" icon="el-icon-document-add" size="mini" @click="createPlan">创建计划</el-button>
  </div>
</template>

<script>

export default {
  name: 'PlanFilterBar',
  data() {
    return {
    }
  },
  methods: {
    async nameFilterAsync(queryString, cb) {},
    handleFilter() {
      this.$emit('refresh')
    },
    createPlan() {
      this.$store.commit('test/CREATE_PLAN_TYPE', '新建计划')
      this.$store.commit('test/RESET_PLAN_FORM', null)
      this.$store.commit('test/SET_ACTIVE', 0)
      return this.$store.commit('test/CREATE_PLAN_VISIBLE', true)
    }
  },
  props: {
    listQuery: {
      required: true,
      type: Object,
      default: () => {
        return this.$cloneDeep(this.$store.state.common.defaultListQuery)
      }
    }
  }
}
</script>

<style scoped>

</style>
