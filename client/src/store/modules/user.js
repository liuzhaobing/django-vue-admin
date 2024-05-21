import { login, logout, getInfo, getUserList } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'
import { arrayToMap } from '@/utils/common'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: '',
    users: [],
    usersIdName: {},
    perms: []
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_USERS: (state, users) => {
    state.users = users
    state.usersIdName = arrayToMap(users, 'id', 'name')
  },
  SET_PERMS: (state, perms) => {
    state.perms = perms
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        commit('SET_TOKEN', data.access)
        setToken(data.access)
        resolve()

      }).catch(error => {
        reject(error)
      })
    })
  },

  getUserList({ commit }, query) {
    return new Promise((resolve, reject) => {
      getUserList(query).then(response => {
        const { data } = response
        const { results } = data
        commit('SET_USERS', results)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { data } = response

        if (!data) {
          reject('验证失败,重新登录.')
        }

        const { perms, name, avatar } = data

        // perms must be a non-empty array
        if (!perms || perms.length <= 0) {
          reject('没有任何权限!')
        }

        commit('SET_PERMS', perms)
        commit('SET_NAME', name)
        commit('SET_AVATAR', avatar)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

