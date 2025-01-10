<template>
  <div class="space-y-4 mb-8">
    <!-- 搜索框 -->
    <div class="relative">
      <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground h-4 w-4" />
      <Input
        v-model="searchQuery"
        :placeholder="$t('post.search')"
        class="pl-9"
        @input="$emit('update:search', searchQuery)"
      />
    </div>

    <!-- 标签列表 -->
    <div class="flex flex-wrap gap-2">
      <Button
        variant="outline"
        size="sm"
        :class="[
          'hover:bg-primary hover:text-primary-foreground transition-colors',
          selectedTag === null ? 'bg-primary text-primary-foreground' : ''
        ]"
        @click="$emit('update:selectedTag', null)"
      >
        {{ $t('post.all') }}
      </Button>
      <Button
        v-for="tag in tags"
        :key="tag"
        variant="outline"
        size="sm"
        :class="[
          'hover:bg-primary hover:text-primary-foreground transition-colors',
          selectedTag === tag ? 'bg-primary text-primary-foreground' : ''
        ]"
        @click="$emit('update:selectedTag', tag)"
      >
        {{ tag }}
      </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Search } from 'lucide-vue-next'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

defineProps<{
  tags: string[]
  selectedTag: string | null
}>()

const searchQuery = ref('')

defineEmits<{
  (e: 'update:search', value: string): void
  (e: 'update:selectedTag', value: string | null): void
}>()
</script> 