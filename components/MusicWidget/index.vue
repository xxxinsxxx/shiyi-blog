<template>
  <div class="space-y-4">
    <!-- 音乐信息 -->
    <div class="flex items-center space-x-4">
      <img :src="currentTrack.cover" class="w-16 h-16 rounded-lg object-cover" :alt="currentTrack.title" />
      <div>
        <h3 class="font-medium">{{ currentTrack.title }}</h3>
        <p class="text-sm text-muted-foreground">{{ currentTrack.artist }}</p>
      </div>
    </div>

    <!-- 进度条 -->
    <div class="space-y-2">
      <div 
        ref="progressBarRef"
        class="relative h-1.5 bg-muted rounded-full overflow-hidden cursor-pointer group"
        @mousedown="startDragging"
        @mousemove="onDragging"
        @mouseup="stopDragging"
        @mouseleave="stopDragging"
        @click="seek"
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
        <span>{{ formatTime(currentTime) }}</span>
        <span>{{ formatTime(duration) }}</span>
      </div>
    </div>

    <!-- 控制按钮 -->
    <div class="flex items-center justify-center space-x-4">
      <Button variant="ghost" size="icon" @click="previousTrack">
        <SkipBack class="h-5 w-5" />
      </Button>
      <Button variant="ghost" size="icon" class="h-10 w-10" @click="togglePlay">
        <Play v-if="!isPlaying" class="h-6 w-6" />
        <Pause v-else class="h-6 w-6" />
      </Button>
      <Button variant="ghost" size="icon" @click="nextTrack">
        <SkipForward class="h-5 w-5" />
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Play, Pause, SkipBack, SkipForward } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'

interface Track {
  id: number
  title: string
  artist: string
  cover: string
  source: string
  type: 'local' | 'api'
}

// 本地音乐列表
const playlist = ref<Track[]>([
  {
    id: 1,
    title: "WILDFLOWER",
    artist: "Billie Eilish",
    cover: "/WILDFLOWER-Billie Eilish.jpg", // 放在 public 目录下的封面图
    source: "/WILDFLOWER-Billie Eilish.mp3", // 放在 public 目录下的音乐文件
    type: 'local'
  },
  // 可以添加更多音乐...
])

const audio = ref<HTMLAudioElement>()
const currentTrackIndex = ref(0)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const progress = computed(() => (currentTime.value / duration.value) * 100 || 0)

// 当前播放的音乐
const currentTrack = computed(() => playlist.value[currentTrackIndex.value])

const progressBarRef = ref<HTMLElement>()
const isDragging = ref(false)

onMounted(() => {
  // 创建音频实例
  audio.value = new Audio()
  
  // 设置音频源
  audio.value.src = currentTrack.value.source

  // 监听事件
  audio.value.addEventListener('timeupdate', updateProgress)
  audio.value.addEventListener('loadedmetadata', () => {
    duration.value = audio.value?.duration || 0
  })
  audio.value.addEventListener('ended', () => {
    nextTrack()
  })
})

onUnmounted(() => {
  // 清理事件监听
  if (audio.value) {
    audio.value.removeEventListener('timeupdate', updateProgress)
    audio.value.pause()
  }
})

// 更新进度
function updateProgress() {
  if (audio.value && !isDragging.value) {
    currentTime.value = audio.value.currentTime
  }
}

// 播放/暂停
function togglePlay() {
  if (!audio.value) return
  
  if (isPlaying.value) {
    audio.value.pause()
  } else {
    audio.value.play()
  }
  isPlaying.value = !isPlaying.value
}

// 上一首
function previousTrack() {
  currentTrackIndex.value = (currentTrackIndex.value - 1 + playlist.value.length) % playlist.value.length
  loadTrack()
}

// 下一首
function nextTrack() {
  currentTrackIndex.value = (currentTrackIndex.value + 1) % playlist.value.length
  loadTrack()
}

// 加载音乐
function loadTrack() {
  if (!audio.value) return
  
  audio.value.src = currentTrack.value.source
  audio.value.load()
  if (isPlaying.value) {
    audio.value.play()
  }
}

// 格式化时间
function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 开始拖动
function startDragging(e: MouseEvent) {
  isDragging.value = true
  seek(e)
}

// 拖动中
function onDragging(e: MouseEvent) {
  if (isDragging.value) {
    seek(e)
  }
}

// 停止拖动
function stopDragging() {
  isDragging.value = false
}

// 跳转到指定位置
function seek(e: MouseEvent) {
  if (!progressBarRef.value || !audio.value) return
  
  const rect = progressBarRef.value.getBoundingClientRect()
  const percent = (e.clientX - rect.left) / rect.width
  const seekTime = percent * duration.value
  
  // 更新进度
  currentTime.value = seekTime
  audio.value.currentTime = seekTime
}
</script>

<style scoped>
/* 防止拖动时选中文本 */
.progress-bar {
  user-select: none;
}
</style>