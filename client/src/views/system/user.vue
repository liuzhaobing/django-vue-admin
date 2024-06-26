<template>
  <div class="app-container">
    <el-row :gutter="10">
      <el-col :md="6">
        <el-card>
          <div slot="header" class="clearfix">
            <span>部门</span>
          </div>
          <el-input v-model="filterOrgText" placeholder="输入部门名进行过滤" />

          <el-tree
            ref="tree"
            v-loading="treeLoding"
            class="filter-tree"
            :data="orgData"
            default-expand-all
            highlight-current
            :expand-on-click-node="false"
            :filter-node-method="filterNode"
            style="margin-top:6px;"
            @node-click="handleOrgClick"
          />
        </el-card>
      </el-col>
      <el-col :md="18">
        <el-card>
          <div slot="header" class="clearfix">
            <span>用户</span>
          </div>
          <div>
            <el-select
              v-model="listQuery.is_active"
              placeholder="状态"
              clearable
              style="width: 90px"
              class="filter-item"
              @change="handleFilter"
            >
              <el-option
                v-for="item in enabledOptions"
                :key="item.key"
                :label="item.display_name"
                :value="item.key"
              />
            </el-select>
            <el-input
              v-model="listQuery.name"
              placeholder="姓名"
              style="width: 200px;"
              class="filter-item"
              @keyup.enter.native="handleFilter"
            />
            <el-button
              class="filter-item"
              type="primary"
              icon="el-icon-search"
              size="mini"
              @click="handleFilter"
            >搜索</el-button>
            <el-button
              class="filter-item"
              type="primary"
              icon="el-icon-refresh-left"
              size="mini"
              @click="resetFilter"
            >重置</el-button>
            <el-button v-if="checkPermission(['user_create'])" type="primary" icon="el-icon-plus" size="mini" @click="handleAddUser">新增</el-button>
          </div>
          <el-table
            v-loading="listLoading"
            v-el-height-adaptive-table="{bottomOffset: 50}"
            :data="userList.results"
            style="width: 100%;margin-top:6px;"
            highlight-current-row
            row-key="id"
            height="100"
            stripe
            border
          >
            <el-table-column type="index" width="50" />
            <el-table-column align="header-center" label="账号">
              <template slot-scope="scope">{{ scope.row.username }}</template>
            </el-table-column>
            <el-table-column align="center" label="姓名">
              <template slot-scope="scope">{{ scope.row.name }}</template>
            </el-table-column>
            <el-table-column align="header-center" label="部门">
              <template
                v-if="scope.row.dept_name != null"
                slot-scope="scope"
              >{{ scope.row.dept_name }}</template>
            </el-table-column>
            <el-table-column label="邮箱">
              <template slot-scope="scope">
                <span>{{ scope.row.email }}</span>
              </template>
            </el-table-column>
            <el-table-column align="center" label="操作">
              <template slot-scope="scope">
                <el-button
                  v-if="!scope.row.is_superuser"
                  :disabled="!checkPermission(['user_update'])"
                  type="primary"
                  size="mini"
                  icon="el-icon-edit"
                  @click="handleEdit(scope)"
                />
                <el-button
                  v-if="!scope.row.is_superuser"
                  :disabled="!checkPermission(['user_delete'])"
                  type="danger"
                  size="mini"
                  icon="el-icon-delete"
                  @click="handleDelete(scope)"
                />
              </template>
            </el-table-column>
          </el-table>

          <pagination
            v-show="userList.count>0"
            :total="userList.count"
            :page.sync="listQuery.page"
            :limit.sync="listQuery.page_size"
            @pagination="getList"
          />
        </el-card>
      </el-col>
    </el-row>

    <el-dialog :visible.sync="dialogVisible" :title="dialogType==='edit'?'编辑用户':'新增用户'">
      <el-form ref="Form" :model="user" label-width="80px" label-position="right" :rules="rule1">
        <el-form-item label="账号" prop="username">
          <el-input v-model="user.username" placeholder="账号/工号" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="user.name" placeholder="姓名" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="user.phone" placeholder="手机号" />
        </el-form-item>
        <el-form-item label="邮箱地址" prop="email">
          <el-input v-model="user.email" placeholder="邮箱地址" />
        </el-form-item>
        <el-form-item label="所属部门" prop="dept">
          <treeselect v-model="user.dept" :multiple="false" :options="orgData" placeholder="所属部门" />
        </el-form-item>
        <el-form-item label="角色" prop="roles">
          <el-select v-model="user.roles" multiple placeholder="请选择" style="width:100%">
            <el-option
              v-for="item in roles"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer">
        <el-button type="danger" @click="dialogVisible=false">取消</el-button>
        <el-button type="primary" @click="confirm('Form')">确认</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<style>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}
.avatar {
  width: 100px;
  height: 100px;
  display: block;
}
</style>
<script>
import { getUserList, createUser, deleteUser, updateUser } from '@/api/user'
import { getOrgAll } from '@/api/org'
import { getRoleAll } from '@/api/role'
import { genTree } from '@/utils'
import checkPermission from '@/utils/permission'
import { upUrl, upHeaders } from '@/api/file'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
const defaultUser = {
  id: '',
  name: '',
  username: '',
  phone: '',
  email: '',
  dept: null,
  avatar: '/media/default/avatar.png'
}
export default {
  components: { Pagination, Treeselect },
  data() {
    return {
      user: defaultUser,
      upHeaders: upHeaders(),
      upUrl: upUrl(),
      userList: { count: 0 },
      roles: [],
      listLoading: true,
      listQuery: {
        page: 1,
        page_size: 20
      },
      enabledOptions: [
        { key: 'true', display_name: '激活' },
        { key: 'false', display_name: '禁用' }
      ],
      dialogVisible: false,
      dialogType: 'new',
      rule1: {
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        username: [{ required: true, message: '请输入账号', trigger: 'change' }],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'change' },
          { pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ]
        // password: [
        //   { required: true, message: '请输入密码', trigger: 'change' }
        // ],
      },
      filterOrgText: '',
      treeLoding: false,
      orgData: []
    }
  },
  computed: {},
  watch: {
    filterOrgText(val) {
      this.$refs.tree.filter(val)
    }
  },
  created() {
    this.getList()
    this.getOrgAll()
    this.getRoleAll()
  },
  methods: {
    checkPermission,
    handleAvatarSuccess(res, file) {
      this.user.avatar = res.data.path
    },
    beforeAvatarUpload(file) {
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isLt2M
    },
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    handleOrgClick(obj, node, vue) {
      this.listQuery.page = 1
      this.listQuery.dept = obj.id
      this.getList()
    },
    getList() {
      this.listLoading = true
      getUserList(this.listQuery).then(response => {
        if (response.data) {
          this.userList = response.data
        }
        this.listLoading = false
      })
    },
    getOrgAll() {
      this.treeLoding = true
      getOrgAll().then(response => {
        this.orgData = genTree(response.data)
        this.treeLoding = false
      })
    },
    getRoleAll() {
      getRoleAll().then(response => {
        this.roles = genTree(response.data)
      })
    },
    resetFilter() {
      this.listQuery = {
        page: 1,
        page_size: 20
      }
      this.getList()
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleAddUser() {
      this.user = Object.assign({}, defaultUser)
      this.dialogType = 'new'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleEdit(scope) {
      this.user = Object.assign({}, scope.row) // copy obj
      this.dialogType = 'edit'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs['Form'].clearValidate()
      })
    },
    handleDelete(scope) {
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          await deleteUser(scope.row.id)
          this.userList.splice(scope.row.index, 1)
          this.$message({
            type: 'success',
            message: '成功删除!'
          })
        })
        .catch(err => {
          console.error(err)
        })
    },
    async confirm(form) {
      this.$refs[form].validate(valid => {
        if (valid) {
          const isEdit = this.dialogType === 'edit'
          if (isEdit) {
            updateUser(this.user.id, this.user).then(res => {
              this.getList()
              this.dialogVisible = false
              this.$message({
                message: '编辑成功',
                type: 'success'
              })
            })
          } else {
            createUser(this.user).then(res => {
              this.getList()
              this.dialogVisible = false
              this.$message({
                message: '新增成功',
                type: 'success'
              })
            })
          }
        } else {
          return false
        }
      })
    }
  }
}
</script>
