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
          <img
            :src="movie.poster"
            :alt="movie.title"
            class="absolute inset-0 w-full h-full object-cover"
            referrerpolicy="no-referrer"
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
import { Star } from 'lucide-vue-next'
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

defineProps<{
  movie: Movie | null
}>()

defineEmits<{
  (e: 'close'): void
}>()
</script>
