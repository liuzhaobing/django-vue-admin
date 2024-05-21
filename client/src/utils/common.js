export function copy(val) {
  const cInput = document.createElement('textarea')
  cInput.value = val.replace(/\n/g, '\n')
  document.body.appendChild(cInput)
  cInput.select()
  try {
    const successful = document.execCommand('copy')
    if (successful) {
      this.$message({
        type: 'success',
        message: '复制成功'
      })
    } else {
      this.$message({
        type: 'error',
        message: '复制失败，请手动复制'
      })
    }
  } catch (err) {
    console.error('复制失败:', err)
    this.$message({
      type: 'error',
      message: '复制失败，请手动复制'
    })
  }
  document.body.removeChild(cInput)
}

export function arrayToMap(array, key, value) {
  const obj = {}
  if (!array) {
    return obj
  }
  for (let i = 0; i < array.length; i++) {
    const item = array[i]
    if (item && typeof item === 'object' && 'id' in item && 'name' in item) {
      obj[item[key]] = item[value]
    }
  }
  return obj
}
