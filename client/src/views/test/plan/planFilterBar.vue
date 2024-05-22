<template>
  <div class="filter-container">
    <el-select
      v-model="listQuery.group"
      clearable
      filterable
      placeholder="分组搜索"
      round
      size="mini"
      style="width: 150px;"
      @change="handleFilter"
    >
      <el-option v-for="(item, index) in groupList" :key="index" :value="item.id" :label="item.name" />
    </el-select>
    <el-select
      v-model="listQuery.type"
      clearable
      placeholder="类型搜索"
      round
      size="mini"
      style="width: 150px;"
      @change="handleFilter"
    >
      <el-option v-for="(item, index) in typeList" :key="index" :value="item.id" :label="item.name" />
    </el-select>
    <el-select
      v-model="listQuery.user"
      clearable
      placeholder="创建者搜索"
      round
      size="mini"
      style="width: 150px;"
      @change="handleFilter"
    >
      <el-option v-for="(item, index) in userList" :key="index" :value="item.id" :label="item.name" />
    </el-select>
    <el-autocomplete
      v-model="listQuery.name"
      :fetch-suggestions="nameFilterAsync"
      placeholder="名称搜索"
      clearable
      size="mini"
      style="width: 350px;"
      @select="handleFilter"
    >
      <i slot="suffix" class="el-input__icon el-icon-search" @click="handleFilter" />
    </el-autocomplete>
    <el-button type="primary" icon="el-icon-refresh" size="mini" @click="handleFilter">刷新</el-button>
    <el-button type="primary" icon="el-icon-document-add" size="mini" @click="createPlan">新增任务</el-button>
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
    },
    userList: {
      required: true,
      type: Array,
      default: () => []
    },
    typeList: {
      required: true,
      type: Array,
      default: () => []
    },
    groupList: {
      required: true,
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>

</style>
