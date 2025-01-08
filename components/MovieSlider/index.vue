<template>
  <div class="relative overflow-hidden">
    <button 
      @click="scroll('left')" 
      class="absolute left-0 top-1/2 -translate-y-1/2 bg-background/80 p-2 rounded-full shadow-lg"
    >
      <ChevronLeft class="w-6 h-6" />
    </button>
    
    <div ref="scrollContainer" class="flex space-x-4 overflow-x-auto pb-4 scroll-smooth">
      <div v-for="movie in movies" :key="movie.id" class="flex-none">
        <img 
          :src="movie.poster" 
          :alt="movie.title"
          class="w-32 h-48 object-cover rounded-lg"
        />
      </div>
    </div>

    <button 
      @click="scroll('right')" 
      class="absolute right-0 top-1/2 -translate-y-1/2 bg-background/80 p-2 rounded-full shadow-lg"
    >
      <ChevronRight class="w-6 h-6" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
defineProps<{
    movies: Array<{
      id: number
      title: string
      poster: string
    }>
  }>()
  
const scrollContainer = ref<HTMLElement>()

function scroll(direction: 'left' | 'right') {
  if (!scrollContainer.value) return
  const scrollAmount = 300
  scrollContainer.value.scrollBy({
    left: direction === 'left' ? -scrollAmount : scrollAmount,
    behavior: 'smooth'
  })
}
</script>