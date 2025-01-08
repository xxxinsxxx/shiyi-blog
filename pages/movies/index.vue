<template>
  <main class="container mx-auto p-4 md:p-6 lg:p-8">
    <!-- 返回按钮 -->
    <NuxtLink to="/" class="inline-flex items-center mb-6 text-muted-foreground hover:text-foreground">
      <ArrowLeft class="w-4 h-4 mr-2" />
      Back to Home
    </NuxtLink>

    <h1 class="text-3xl font-bold mb-8">Movies</h1>

    <!-- 电影海报墙 -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
      <button
        v-for="movie in movies"
        :key="movie.id"
        @click="openMovieDialog(movie)"
        class="group relative aspect-[2/3] overflow-hidden rounded-lg"
      >
        <img
          :src="movie.poster"
          :alt="movie.title"
          class="absolute inset-0 h-full w-full object-cover transition group-hover:scale-105"
        />
        <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition flex items-end p-4">
          <div class="text-white">
            <h3 class="font-semibold">{{ movie.title }}</h3>
            <p class="text-sm text-gray-300">{{ movie.year }}</p>
          </div>
        </div>
      </button>
    </div>

    <!-- 电影详情弹窗 -->
    <Dialog :open="!!selectedMovie" @update:open="closeMovieDialog">
      <DialogContent class="sm:max-w-[800px]">
        <DialogHeader>
          <DialogTitle>{{ selectedMovie?.title }}</DialogTitle>
          <DialogDescription>{{ selectedMovie?.year }}</DialogDescription>
        </DialogHeader>
        
        <div v-if="selectedMovie" class="grid md:grid-cols-[300px,1fr] gap-6 mt-4">
          <!-- 电影海报 -->
          <div class="aspect-[2/3] relative rounded-lg overflow-hidden">
            <img 
              :src="selectedMovie.poster" 
              :alt="selectedMovie.title" 
              class="absolute inset-0 w-full h-full object-cover" 
            />
          </div>

          <!-- 电影信息 -->
          <div class="space-y-6">
            <div class="flex items-center space-x-2">
              <Star class="w-5 h-5 fill-yellow-400 stroke-yellow-400" />
              <span class="text-lg font-semibold">{{ selectedMovie.rating }}/10</span>
            </div>

            <div>
              <h2 class="text-lg font-semibold mb-2">Overview</h2>
              <p class="text-muted-foreground">{{ selectedMovie.description }}</p>
            </div>

            <div>
              <h2 class="text-lg font-semibold mb-2">Director</h2>
              <p class="text-muted-foreground">{{ selectedMovie.director }}</p>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button @click="closeMovieDialog">Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </main>
</template>

<script setup lang="ts">
import { ArrowLeft, Star } from 'lucide-vue-next'
import { 
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

interface Movie {
  id: number
  title: string
  year: string
  poster: string
  description: string
  director: string
  rating: number
}

// 模拟电影数据，实际应该从API获取
const movies = ref<Movie[]>([
  {
    id: 1,
    title: "Inception",
    year: "2010",
    poster: "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
    description: "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    director: "Christopher Nolan",
    rating: 8.8
  },
  {
    id: 2,
    title: "The Dark Knight",
    year: "2008",
    poster: "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    description: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
    director: "Christopher Nolan",
    rating: 9.0
  },
  // 添加更多电影...
])

const selectedMovie = ref<Movie | null>(null)

function openMovieDialog(movie: Movie) {
  selectedMovie.value = movie
}

function closeMovieDialog() {
  selectedMovie.value = null
}
</script> 