<template>
  <Dialog :open="!!movie" @update:open="$emit('close')">
    <DialogContent class="md:max-w-[800px] overflow-y-auto max-h-[80vh] max-w-[80vw] rounded-lg">
      <DialogHeader class="relative">
        <DialogTitle class="text-2xl">{{ movie?.title }}</DialogTitle>
        <DialogDescription>{{ movie?.year }}</DialogDescription>
        <DialogClose class="absolute right-0 top-0 focus:!ring-0" />
      </DialogHeader>

      <div v-if="movie" class="grid grid-cols-1 md:grid-cols-[300px,1fr] gap-6 mt-4">
        <!-- 电影海报 -->
        <div class="aspect-[2/3] relative rounded-lg overflow-hidden w-[200px] mx-auto md:w-full">
          <div class="absolute inset-0 bg-gray-200 animate-pulse" v-if="isImageLoading"></div>
          <div v-if="imageError" class="absolute inset-0 flex items-center justify-center bg-gray-100">
            <div class="text-center p-4">
              <ImageOff class="w-10 h-10 mx-auto text-gray-400 mb-2" />
              <p class="text-sm text-gray-500">{{ $t('common.imageLoadError') || '图片加载失败' }}</p>
            </div>
          </div>
          <img
            :src="movie.poster"
            :alt="movie.title"
            class="absolute inset-0 w-full h-full object-cover"
            referrerpolicy="no-referrer"
            @load="handleImageLoad"
            @error="handleImageError"
            :class="{ 'opacity-0': isImageLoading || imageError }"
          />
        </div>

        <!-- 电影信息 -->
        <div class="space-y-6">
          <!-- 评分 -->
          <div class="flex items-center justify-center md:justify-start space-x-6">
            <div class="flex items-center space-x-2">
              <img src="/douban.png" class="w-5 h-5" alt="douban" />
              <span class="text-lg font-semibold">{{ movie.doubanRating }}/10</span>
            </div>
            <div class="flex items-center space-x-2">
              <Star class="w-5 h-5 fill-yellow-400 stroke-yellow-400" />
              <span class="text-lg font-semibold">{{ movie?.myRating || "-" }}/10</span>
            </div>
          </div>

          <div>
            <h2 class="text-lg font-semibold mb-2">{{ $t('movie.overview') }}</h2>
            <p class="text-muted-foreground ">{{ movie.description }}</p>
          </div>

          <div>
            <h2 class="text-lg font-semibold mb-2">{{ $t('movie.director') }}</h2>
            <p class="text-muted-foreground">{{ movie.director }}</p>
          </div>

          <!-- 我的评语 -->
          <div v-if="movie.comment">
            <h2 class="text-lg font-semibold mb-2">{{ $t('movie.myComment') }}</h2>
            <p class="text-muted-foreground">{{ movie.comment }}</p>
          </div>
        </div>
      </div>

    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { Star, ImageOff } from 'lucide-vue-next'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

interface Movie {
  id: number
  title: string
  year: string
  poster: string
  description: string
  director: string
  doubanRating: number
  myRating: number
  comment: string
}

const props = defineProps<{
  movie: Movie | null
}>()

defineEmits<{
  (e: 'close'): void
}>()

const isImageLoading = ref(true)
const imageError = ref(false)

// 监听 movie 变化，重置图片状态
watch(() => props.movie, () => {
  if (props.movie) {
    isImageLoading.value = true
    imageError.value = false
  }
}, { immediate: true })

function handleImageLoad() {
  isImageLoading.value = false
}

function handleImageError() {
  isImageLoading.value = false
  imageError.value = true
  
  // 可选：尝试使用备用图片或重试加载
  if (props.movie && !props.movie.poster.includes('retry')) {
    setTimeout(() => {
      if (props.movie) {
        // 这里我们不能直接修改 props，但可以通过事件通知父组件
        // 或者在实际应用中，你可能会使用其他方式处理
        imageError.value = false
        isImageLoading.value = true
      }
    }, 1000)
  }
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
