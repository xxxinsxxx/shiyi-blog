<template>
    <Transition name="slide">
        <div 
      v-if="player && player.currentTrack && player.showFloating"
      :class="[
        'fixed z-50 transition-all duration-300',
        player.isMinimized 
          ? 'bottom-4 right-4 w-16 h-16' 
          : 'bottom-4 right-4 w-80 bg-card shadow-lg rounded-lg p-4'
      ]"
    >
        <!-- 最小化状态 -->
        <button
          v-if="player.isMinimized"
          @click="player.toggleMinimize"
          class="w-full h-full rounded-full bg-primary/10 hover:bg-primary/20 transition flex items-center justify-center group"
        >
          <img 
            :src="player.currentTrack?.cover" 
            class="w-12 h-12 rounded-full object-cover group-hover:animate-[spin_5s_linear_infinite]"
            :class="{ 'animate-[spin_5s_linear_infinite]': player.isPlaying }"
          />
        </button>
  
        <!-- 展开状态 -->
        <div v-else class="space-y-4">
          <!-- 标题栏 -->
          <div class="flex items-center justify-between">
            <h3 class="font-medium">Now Playing</h3>
            <button 
              @click="player.toggleMinimize"
              class="text-muted-foreground hover:text-foreground"
            >
              <Minimize class="w-4 h-4" />
            </button>
          </div>
  
          <!-- 音乐信息 -->
          <div class="flex items-center space-x-4">
            <img 
              :src="player.currentTrack?.cover" 
              class="w-16 h-16 rounded-lg object-cover"
            />
            <div>
              <h4 class="font-medium">{{ player.currentTrack?.title }}</h4>
              <p class="text-sm text-muted-foreground">{{ player.currentTrack?.artist }}</p>
            </div>
          </div>
  
          <!-- 进度条 -->
          <div class="space-y-2">
            <div 
              ref="progressBarRef"
              class="relative h-1.5 bg-muted rounded-full overflow-hidden cursor-pointer"
              @click="seek"
            >
              <div 
                class="absolute h-full bg-primary transition-all duration-100"
                :style="{ width: `${progress}%` }"
              />
            </div>
            <div class="flex justify-between text-xs text-muted-foreground">
              <span>{{ formatTime(player.currentTime) }}</span>
              <span>{{ formatTime(player.duration) }}</span>
            </div>
          </div>
  
          <!-- 控制按钮 -->
          <div class="flex items-center justify-center space-x-4">
            <Button variant="ghost" size="icon" @click="player.previousTrack">
              <SkipBack class="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" class="h-10 w-10" @click="player.togglePlay">
              <Play v-if="!player.isPlaying" class="h-6 w-6" />
              <Pause v-else class="h-6 w-6" />
            </Button>
            <Button variant="ghost" size="icon" @click="player.nextTrack">
              <SkipForward class="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </Transition>
  </template>
  
  <script setup lang="ts">
  import { Play, Pause, SkipBack, SkipForward, Minimize } from 'lucide-vue-next'
  import { Button } from '@/components/ui/button'
  import { usePlayerStore } from '@/stores/player'
  import { useRoute } from 'vue-router'
  
// 使用 ref 来存储 store 实例
const player = ref()
const route = useRoute()

// 在客户端初始化 store
onMounted(() => {
  player.value = usePlayerStore()
  player.value.initAudio()
})

// 监听路由变化
watch(() => route.path, (newPath) => {
  if (player.value) {
    // 在首页隐藏悬浮播放器，其他页面显示
    player.value.setShowFloating(newPath !== '/')
  }
}, { immediate: true })
  const progressBarRef = ref<HTMLElement>()
  
  // 计算进度百分比
  const progress = computed(() => 
    (player.value.currentTime / player.value.duration) * 100 || 0
  )
  
  // 格式化时间
  function formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }
  
  // 跳转播放位置
  function seek(e: MouseEvent) {
    if (!progressBarRef.value) return
    const rect = progressBarRef.value.getBoundingClientRect()
    const percent = (e.clientX - rect.left) / rect.width
    player.value.seek(percent * player.value.duration)
  }
  
  // 在组件挂载时初始化音频
  onMounted(() => {
    player.value.initAudio()
  })
  </script>
  
  <style scoped>
  .slide-enter-active,
  .slide-leave-active {
    transition: all 0.3s ease;
  }
  
  .slide-enter-from,
  .slide-leave-to {
    transform: translateY(100%);
    opacity: 0;
  }
  </style>