<template>
  <main class="container mx-auto p-4 md:p-6 lg:p-8">
    <!-- 返回按钮 -->
    <button 
      @click="router.back()" 
      class="inline-flex items-center mb-6 text-muted-foreground hover:text-foreground"
    >
      <ArrowLeft class="w-4 h-4 mr-2" />
      Back
    </button>

    <article class="prose dark:prose-invert mx-auto">
      <header class="mb-8">
        <h1 class="text-3xl font-bold">{{ data?.title }}</h1>
        <div class="flex items-center space-x-4 text-muted-foreground mt-4">
          <time v-if="data?.date">{{ formatDate(data.date) }}</time>
          <template v-if="data?.description">
            <span>·</span>
            <span>{{ data.description }}</span>
          </template>
        </div>
      </header>
      
      <ContentRenderer v-if="data" :value="data" />
    </article>
  </main>
</template>

<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'

const router = useRouter()
const { path } = useRoute()

// 获取文章内容
const { data } = await useAsyncData(`content-${path}`, () => {
  return queryContent().where({ _path: path }).findOne()
})

// 如果文章不存在，返回404
if (!data.value) {
  throw createError({
    statusCode: 404,
    message: 'Article not found'
  })
}

// 格式化日期
function formatDate(date: string) {
  try {
    // 确保日期格式正确（YYYY-MM-DD）
    const dateObj = new Date(date)
    if (isNaN(dateObj.getTime())) {
      return 'No date'
    }
    
    return dateObj.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
    console.error('Date parsing error:', e)
    return 'Invalid date'
  }
}
</script>

<style scoped>
.prose {
  max-width: 65ch;
}
</style> 