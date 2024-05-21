<template>
  <el-dialog
    :title="$store.state.test.createPlanType"
    :visible.sync="$store.state.test.createPlanVisible"
    :before-close="onDialogClose"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    width="750px"
    append-to-body
  >
    <el-steps :active="active" finish-status="success" align-center style="margin-bottom: 30px">
      <el-step title="环境配置" />
      <el-step title="数据源选择" />
      <el-step title="基础信息" />
    </el-steps>
    <el-form
      ref="ruleForm"
      :model="$store.state.test.createPlanForm"
      :rules="rules"
      label-width="100px"
      autocomplete="off"
      size="medium"
      style="margin-right: 30px"
    >
      <div v-if="active === 0"></div>
      <div v-if="active === 1"></div>
      <div v-if="active === 2"></div>
    </el-form>
    <div class="footer" align="right" style="padding-top:10px">
      <el-button
        v-if="active > 0"
        type="info"
        size="small"
        icon="el-icon-arrow-left"
        @click="prev"
      >上一步
      </el-button>
      <el-button
        v-if="active < step - 1"
        type="primary"
        size="small"
        icon="el-icon-arrow-right"
        @click="next"
      >下一步</el-button>
      <el-button size="small" @click="$store.commit('test/CREATE_PLAN_VISIBLE', false)">取 消</el-button>
      <el-button v-if="active === step - 1" type="primary" size="small" @click="submit(true)">确定并立即执行</el-button>
      <el-button v-if="active === step - 1" type="primary" size="small" @click="submit(false)">确 定</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'PlanAddDialog',
  data() {
    return {
      step: 3,
      rules: {},
    }
  },
  computed: {
    active: {
      get() {
        return this.$store.state.test.active
      },
      set(val) {
        this.$store.commit('test/SET_ACTIVE', val)
      }
    }
  },
  methods: {
    onDialogClose(done) {
      done()
    },
    prev() {
      this.active--
    },
    next() {
      this.active++
    },
  }
}

</script>

<style scoped>

</style>
