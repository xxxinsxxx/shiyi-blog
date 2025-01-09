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
            <p class="text-sm text-left text-gray-300">{{ movie.year }}</p>
          </div>
        </div>
      </button>
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

const movies = ref(movieData.movies)
const selectedMovie = ref(null)

function openMovieDialog(movie:any) {
  selectedMovie.value = movie
}

function closeMovieDialog() {
  selectedMovie.value = null
}
</script> 