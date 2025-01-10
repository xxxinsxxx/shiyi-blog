<template>
  <footer class="mt-8 border-t">
    <div class="container mx-auto px-4 py-6">
      <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        <!-- 版权信息 -->
        <div class="text-sm text-muted-foreground">
          © {{ new Date().getFullYear() }} Shiyi. All rights reserved.
        </div>

        <!-- 中间链接 -->
        <div class="flex items-center space-x-4 text-sm text-muted-foreground">
          <a 
            href="https://github.com/yourusername" 
            target="_blank" 
            rel="noopener noreferrer"
            class="hover:text-foreground transition"
          >
            GitHub
          </a>
        </div>

        <!-- 语言切换 -->
        <div class="flex items-center space-x-2">
          <Button
            v-for="locale in $i18n.locales"
            :key="locale.code"
            variant="ghost"
            size="sm"
            :class="[
              'text-sm',
              $i18n.locale === locale.code ? 'text-primary' : 'text-muted-foreground'
            ]"
            @click="$i18n.setLocale(locale.code)"
          >
            {{ locale.name }}
          </Button>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
</script> 