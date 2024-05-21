import { deepClone } from '@/utils'

const getDefaultState = () => {
  return {
    defaultPlanFrom: {
      name: '',
      type: null,
      group: null,
      config: '',
      data_source: '',
    },
    createPlanVisible: false,
    createPlanType: '',
    createPlanForm: {},
    active: 0,
    viewPlanVisible: false,
  }
}

const state = getDefaultState()

const mutations = {
  CREATE_PLAN_VISIBLE(state, visible) {
    state.createPlanVisible = visible
  },
  CREATE_PLAN_TYPE(state, type) {
    state.createPlanType = type
  },
  SET_ACTIVE(state, active) {
    state.active = active
  },
  RESET_PLAN_FORM(state, form) {
    if (!form) {
      state.createPlanForm = deepClone(state.defaultPlanFrom)
    } else {
      state.createPlanForm = deepClone(form)
    }
  },
  CREATE_PLAN_FORM(state, form) {
    state.createPlanForm = form
  },
  VIEW_PLAN_VISIBLE(state, visible) {
    state.viewPlanVisible = visible
  },
}

export default {
  namespaced: true,
  state,
  mutations
}
