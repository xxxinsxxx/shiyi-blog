import { defineStore } from 'pinia'

interface Track {
  id: number
  title: string
  artist: string
  cover: string
  source: string
}

export const usePlayerStore = defineStore('player', {
  state: () => ({
    currentTrack: {
      id: 1,
      title: "WILDFLOWER",
      artist: "Billie Eilish",
      cover: "/WILDFLOWER-Billie Eilish.jpg",
      source: "/WILDFLOWER-Billie Eilish.mp3",
    },
    isPlaying: false,
    currentTime: 0,
    duration: 0,
    isMinimized: true,
    showFloating: false,
    audio: null as HTMLAudioElement | null,
    playlist: [
      {
        id: 1,
        title: "WILDFLOWER",
        artist: "Billie Eilish",
        cover: "/WILDFLOWER-Billie Eilish.jpg",
        source: "/WILDFLOWER-Billie Eilish.mp3",
      }
    ]
  }),

  actions: {
    initAudio() {
      if (process.client && !this.audio) {
        this.audio = new Audio()
        this.audio.src = this.currentTrack.source
        
        this.audio.addEventListener('timeupdate', () => {
          this.currentTime = this.audio?.currentTime || 0
        })
        
        this.audio.addEventListener('loadedmetadata', () => {
          this.duration = this.audio?.duration || 0
        })
        
        this.audio.addEventListener('ended', this.nextTrack)
      }
    },

    togglePlay() {
      if (!this.audio) {
        this.initAudio()
      }
      
      if (this.isPlaying) {
        this.audio?.pause()
      } else {
        this.audio?.play()
      }
      this.isPlaying = !this.isPlaying
    },

    seek(time: number) {
      if (this.audio) {
        this.audio.currentTime = time
        this.currentTime = time
      }
    },

    nextTrack() {
      const currentIndex = this.playlist.findIndex(track => track.id === this.currentTrack.id)
      const nextIndex = (currentIndex + 1) % this.playlist.length
      this.currentTrack = this.playlist[nextIndex]
      if (this.audio) {
        this.audio.src = this.currentTrack.source
        if (this.isPlaying) {
          this.audio.play()
        }
      }
    },

    previousTrack() {
      const currentIndex = this.playlist.findIndex(track => track.id === this.currentTrack.id)
      const prevIndex = (currentIndex - 1 + this.playlist.length) % this.playlist.length
      this.currentTrack = this.playlist[prevIndex]
      if (this.audio) {
        this.audio.src = this.currentTrack.source
        if (this.isPlaying) {
          this.audio.play()
        }
      }
    },

    toggleMinimize() {
      this.isMinimized = !this.isMinimized
    },

    setShowFloating(show: boolean) {
      this.showFloating = show
    }
  }
})