<template>
  <main class="container p-4 md:p-6 lg:p-8">
    <!-- 返回按钮 -->
    <NuxtLink to="/" class="inline-flex items-center mb-6 text-muted-foreground hover:text-foreground">
      <ArrowLeft class="w-4 h-4 mr-2" />
      {{ $t('post.backToHome') }}
    </NuxtLink>

    <h1 class="text-3xl font-bold mb-8">{{ $t('nav.movies') }}</h1>

    <!-- 电影海报墙 -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <button
        v-for="movie in displayedMovies"
        :key="movie.id"
        @click="openMovieDialog(movie)"
        class="group relative aspect-[2/3] overflow-hidden rounded-lg"
      >
        <div class="absolute inset-0 bg-gray-200 animate-pulse"></div>
        <img
          :src="movie.poster"
          :alt="movie.title"
          referrerpolicy="no-referrer"
          loading="lazy"
          class="absolute inset-0 h-full w-full object-cover transition group-hover:scale-105 opacity-0"
          @error="handleImageError($event, movie)"
          @load="handleImageLoad($event)"
        />
        <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition flex items-end p-4">
          <div class="text-white">
            <h3 class="font-semibold">{{ movie.title }}</h3>
            <p class="text-sm text-left text-gray-300">{{ movie.year }}</p>
          </div>
        </div>
      </button>
    </div>

    <!-- 加载更多指示器 -->
    <div
      v-if="hasMore"
      ref="loadMoreTrigger"
      class="py-8 text-center text-muted-foreground"
    >
      <span v-if="isLoading">{{ $t('common.loading') }}</span>
      <span v-else>{{ $t('common.loadMore') }}</span>
    </div>

    <!-- 使用抽离出的对话框组件 -->
    <MovieDialog
      :movie="selectedMovie"
      @close="closeMovieDialog"
    />
  </main>
</template>

<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import movieData from '@/data/movies.json'

const PAGE_SIZE = 10
const allMovies = ref(movieData.movies)
const currentPage = ref(1)
const isLoading = ref(false)
const loadMoreTrigger = ref(null)
const selectedMovie = ref(null)
const failedImages = ref(new Set())

// 计算当前显示的电影
const displayedMovies = computed(() => {
  return allMovies.value.slice(0, currentPage.value * PAGE_SIZE)
})

// 是否还有更多数据
const hasMore = computed(() => {
  return displayedMovies.value.length < allMovies.value.length
})

// 处理图片加载失败
function handleImageError(event: Event, movie: any) {
  console.error(`Failed to load image for movie: ${movie.title}`)
  failedImages.value.add(movie.id)

  // 尝试重新加载图片
  const img = event.target as HTMLImageElement
  if (!img.dataset.retried) {
    img.dataset.retried = 'true'
    setTimeout(() => {
      img.src = movie.poster + '?retry=' + new Date().getTime()
    }, 1000)
  }
}

// 处理图片加载成功
function handleImageLoad(event: Event) {
  const img = event.target as HTMLImageElement
  // 使用淡入效果显示图片
  img.style.transition = 'opacity 0.3s ease-in-out'
  img.style.opacity = '1'
}

// 加载更多电影
function loadMore() {
  if (isLoading.value || !hasMore.value) return

  isLoading.value = true

  // 模拟网络请求延迟
  setTimeout(() => {
    currentPage.value++
    isLoading.value = false
  }, 500)
}

// 设置 Intersection Observer
onMounted(() => {
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting && hasMore.value && !isLoading.value) {
      loadMore()
    }
  }, {
    rootMargin: '100px'
  })

  if (loadMoreTrigger.value) {
    observer.observe(loadMoreTrigger.value)
  }
})

function openMovieDialog(movie: any) {
  selectedMovie.value = movie
}

function closeMovieDialog() {
  selectedMovie.value = null
}
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 0.8;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
