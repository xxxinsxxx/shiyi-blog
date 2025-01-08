<template>
  <div class="flex items-center space-x-4">
    <div v-if="currentTrack" class="flex items-center space-x-4">
      <img :src="currentTrack.albumArt" class="w-16 h-16 rounded" :alt="currentTrack.name" />
      <div>
        <h3 class="font-medium">{{ currentTrack.name }}</h3>
        <p class="text-sm text-muted-foreground">{{ currentTrack.artist }}</p>
      </div>
    </div>
    <div v-else class="min-h-[100px] flex items-center justify-center text-muted-foreground">
      Not playing
    </div>
  </div>
</template>

<script setup lang="ts">
const currentTrack = ref(null)
// 这里需要添加 Spotify API 集成
</script>