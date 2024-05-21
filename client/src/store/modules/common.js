const getDefaultState = () => {
  return {
    defaultListQuery: { page: 1, page_size: 20 },
  }
}

const state = getDefaultState()
export default {
  namespaced: true,
  state
}
