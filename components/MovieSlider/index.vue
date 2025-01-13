<template>
  <div class="relative overflow-hidden">
    <button
      v-if="showLeftArrow"
      @click="scroll('left')"
      class="absolute left-0 top-1/2 -translate-y-1/2 bg-background/80 p-2 rounded-full shadow-lg z-10 ml-1"
    >
      <ChevronLeft class="w-6 h-6" />
    </button>

    <div
      ref="scrollContainer"
      class="flex space-x-4 overflow-x-auto pb-4 scroll-smooth"
      @scroll="updateArrows"
    >
      <div v-for="movie in movies" :key="movie.id" class="flex-none">
        <button
          @click="openMovieDialog(movie)"
          class="relative group aspect-[2/3] overflow-hidden rounded-lg"
        >
          <img
            :src="movie.poster"
            :alt="movie.title"
             referrerpolicy="no-referrer"
            class="w-32 h-48 object-cover rounded-lg transition group-hover:scale-105"
          />
          <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition flex items-end p-2 rounded-lg">
            <div class="text-white text-left">
              <h3 class="font-semibold text-sm">{{ movie.title }}</h3>
              <p class="text-xs text-gray-300">{{ movie.year }}</p>
            </div>
          </div>
        </button>
      </div>
    </div>

    <button
      v-if="showRightArrow"
      @click="scroll('right')"
      class="absolute right-0 top-1/2 -translate-y-1/2 bg-background/80 p-2 rounded-full shadow-lg  z-10 mr-1"
    >
      <ChevronRight class="w-6 h-6" />
    </button>

    <!-- 使用抽离出的对话框组件 -->
    <MovieDialog
      :movie="selectedMovie"
      @close="closeMovieDialog"
    />
  </div>
</template>

<script setup lang="ts">
import { ChevronLeft, ChevronRight, Star } from 'lucide-vue-next'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import MovieDialog from '@/components/MovieDialog.vue'

interface Movie {
  id: number
  title: string
  year: string
  poster: string
  description: string
  director: string
  rating: number
  comment: string
}

defineProps<{
  movies: Movie[]
}>()

const scrollContainer = ref<HTMLElement>()
const selectedMovie = ref<Movie | null>(null)
const showLeftArrow = ref(false)
const showRightArrow = ref(false)

// 更新箭头显示状态
function updateArrows() {
  if (!scrollContainer.value) return

  const { scrollLeft, scrollWidth, clientWidth } = scrollContainer.value
  showLeftArrow.value = scrollLeft > 0
  showRightArrow.value = scrollLeft + clientWidth < scrollWidth - 1 // -1 是为了处理小数点误差
}

// 在组件挂载和更新时检查是否需要显示箭头
onMounted(() => {
  updateArrows()
})

onUpdated(() => {
  updateArrows()
})

function scroll(direction: 'left' | 'right') {
  if (!scrollContainer.value) return
  const scrollAmount = 300
  scrollContainer.value.scrollBy({
    left: direction === 'left' ? -scrollAmount : scrollAmount,
    behavior: 'smooth'
  })
}

function openMovieDialog(movie: Movie) {
  selectedMovie.value = movie
}

function closeMovieDialog() {
  selectedMovie.value = null
}
</script>
