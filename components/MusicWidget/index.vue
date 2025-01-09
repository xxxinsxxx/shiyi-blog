<template>
  <div v-if="player" class="space-y-4">
    <!-- 音乐信息 -->
    <div class="flex items-center space-x-4">
      <img 
        :src="player.currentTrack?.cover" 
        class="w-16 h-16 rounded-lg object-cover" 
      />
      <div>
        <h3 class="font-medium">{{ player.currentTrack?.title }}</h3>
        <p class="text-sm text-muted-foreground">{{ player.currentTrack?.artist }}</p>
      </div>
    </div>

    <!-- 进度条 -->
    <div class="space-y-2">
      <div 
        ref="progressBarRef"
        class="relative h-1.5 bg-muted rounded-full overflow-hidden cursor-pointer group"
        @click="onProgressClick"
      >
        <div 
          class="absolute h-full bg-primary transition-all duration-100"
          :style="{ width: `${progress}%` }"
        ></div>
        <!-- 进度条拖动点 -->
        <div 
          class="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-primary opacity-0 group-hover:opacity-100 transition-opacity"
          :style="{ left: `calc(${progress}% - 6px)` }"
        ></div>
      </div>
      <div class="flex justify-between text-xs text-muted-foreground">
        <span>{{ formatTime(player?.currentTime || 0) }}</span>
        <span>{{ formatTime(player?.duration || 0) }}</span>
      </div>
    </div>

    <!-- 控制按钮 -->
    <div class="flex items-center justify-center space-x-4">
      <Button variant="ghost" size="icon"  @click="player?.previousTrack()">
        <SkipBack class="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" class="h-10 w-10" @click="player?.togglePlay()">
        <Play v-if="!player?.isPlaying" class="h-6 w-6" />
        <Pause v-else class="h-6 w-6" />
      </Button>
      <Button variant="ghost" size="icon" @click="player?.nextTrack()">
        <SkipForward class="h-5 w-5" />
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Play, Pause, SkipBack, SkipForward } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { usePlayerStore } from '@/stores/player'

// 使用 ref 来存储 store 实例
const player = ref()
const progressBarRef = ref<HTMLElement>()

// 在客户端初始化 store
onMounted(() => {
  player.value = usePlayerStore()
  player.value.initAudio()
})


// 计算进度百分比
const progress = computed(() => 
  ((player.value?.currentTime || 0) / (player.value?.duration || 1)) * 100
)

// 格式化时间
function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 处理进度条点击
function onProgressClick(e: MouseEvent) {
  if (!progressBarRef.value || !player.value) return
  const rect = progressBarRef.value.getBoundingClientRect()
  const percent = (e.clientX - rect.left) / rect.width
  player.value.seek(percent * player.value.duration)
}
</script>

<style scoped>
/* 防止拖动时选中文本 */
.progress-bar {
  user-select: none;
}
</style>