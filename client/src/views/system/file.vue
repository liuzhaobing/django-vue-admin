<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select
        v-model="listQuery.type"
        placeholder="文件类型"
        clearable
        style="width: 200px"
        size="mini"
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
        v-model="listQuery.search"
        placeholder="文件名"
        style="width: 300px;"
        size="mini"
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
      <el-upload
        ref="upload"
        class="upload"
        :action="upUrl"
        :headers="upHeaders"
        :on-success="getList"
        :show-file-list="false"
        :limit="1"
        accept=".xls,.xlsx"
      >
        <el-button type="primary" icon="el-icon-upload2" size="mini">文件上传</el-button>
      </el-upload>
    </div>
    <el-table
      v-loading="listLoading"
      v-el-height-adaptive-table="{bottomOffset: 50}"
      :data="fileList.results"
      style="width: 100%;"
      highlight-current-row
      row-key="id"
      height="100"
      stripe
      border
    >
      <el-table-column type="index" width="50" label="#" />
      <el-table-column align="center" label="名称">
        <template slot-scope="scope">
          <el-link type="primary" :href="scope.row.file" target="_blank">{{ scope.row.name }}</el-link>
        </template>
      </el-table-column>
      <el-table-column align="header-center" label="类型">
        <template slot-scope="scope">{{ scope.row.type }}</template>
      </el-table-column>
      <el-table-column align="header-center" label="格式">
        <template slot-scope="scope">{{ scope.row.mime }}</template>
      </el-table-column>
      <el-table-column align="header-center" label="大小">
        <template slot-scope="scope">{{ formatFileSize(scope.row.size) }}</template>
      </el-table-column>
      <el-table-column align="header-center" label="地址">
        <template slot-scope="scope">{{ scope.row.path }}</template>
      </el-table-column>
      <el-table-column label="上传日期">
        <template slot-scope="scope">
          <span>{{ scope.row.create_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-delete"
            @click="deleteOneFile(scope.row)"
          />
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="fileList.count>0"
      :total="fileList.count"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size"
      @pagination="getList"
    />
  </div>
</template>
<script>
import { getFileList, upHeaders, upUrl, deleteFile } from '@/api/file'
import Pagination from '@/components/Pagination'
export default {
  components: { Pagination },
  data() {
    return {
      upUrl: upUrl(),
      upHeaders: upHeaders(),
      fileList: { count: 0 },
      listLoading: true,
      listQuery: {
        page: 1,
        page_size: 20
      },
      enabledOptions: [
        { key: '文档', display_name: '文档' },
        { key: '图片', display_name: '图片' },
        { key: '音频', display_name: '音频' },
        { key: '视频', display_name: '视频' },
        { key: '其它', display_name: '其它' }
      ]
    }
  },
  created() {
    this.getList()
  },
  methods: {
    formatFileSize(sizeInBytes) {
      const units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
      let unitIndex = 0
      while (sizeInBytes >= 1024 && unitIndex < units.length - 1) {
        sizeInBytes /= 1024
        unitIndex++
      }
      return `${sizeInBytes.toFixed(1)} ${units[unitIndex]}`
    },
    deleteOneFile(row) {
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'error'
      })
        .then(async() => {
          await deleteFile(row.id)
          this.getList()
          this.$message({
            type: 'success',
            message: '成功删除!'
          })
        })
    },
    getList() {
      this.listLoading = true
      getFileList(this.listQuery).then(response => {
        if (response.data) {
          this.fileList = response.data
        }
        this.listLoading = false
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
    }
  }
}
</script>
<style scoped>

</style>
