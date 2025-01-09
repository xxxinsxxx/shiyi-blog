<template>
  <Dialog :open="!!movie" @update:open="$emit('close')">
    <DialogContent class="sm:max-w-[800px]">
      <DialogHeader>
        <DialogTitle>{{ movie?.title }}</DialogTitle>
        <DialogDescription>{{ movie?.year }}</DialogDescription>
        <DialogClose class="focus:!ring-0" />
      </DialogHeader>
      
      <div v-if="movie" class="grid md:grid-cols-[300px,1fr] gap-6 mt-4">
        <!-- 电影海报 -->
        <div class="aspect-[2/3] relative rounded-lg overflow-hidden">
          <img 
            :src="movie.poster" 
            :alt="movie.title" 
            class="absolute inset-0 w-full h-full object-cover" 
          />
        </div>

        <!-- 电影信息 -->
        <div class="space-y-6">
          <!-- 评分 -->
          <div class="flex items-center space-x-6">
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
            <h2 class="text-lg font-semibold mb-2">Overview</h2>
            <p class="text-muted-foreground">{{ movie.description }}</p>
          </div>

          <div>
            <h2 class="text-lg font-semibold mb-2">Director</h2>
            <p class="text-muted-foreground">{{ movie.director }}</p>
          </div>

          <!-- 我的评语 -->
          <div>
            <h2 class="text-lg font-semibold mb-2">My Comment</h2>
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