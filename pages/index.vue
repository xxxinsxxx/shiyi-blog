<template>
  <div class="min-h-screen flex flex-col">
    <main class="container mx-auto p-4 md:p-6 lg:p-8 flex-grow">
      <div class="grid grid-cols-1 md:grid-cols-8 lg:grid-cols-12 gap-4">
        <!-- 左侧栏 -->
        <div class="md:col-span-4 lg:col-span-4 space-y-4">
          <!-- 个人信息 -->
          <Card class="p-4">
            <div class="flex flex-col sm:flex-row items-center  space-y-4 sm:space-y-0 sm:space-x-4">
              <Avatar class="w-24 h-24">
                <AvatarImage src="/avatar.jpg" />
                <AvatarFallback>Shiyi</AvatarFallback>
              </Avatar>
              <div class="text-center sm:text-left flex flex-col justify-between">
                <h1 class="text-2xl font-bold">Shiyi</h1>
                <p class="text-muted-foreground">Frontend Developer</p>
                <a class="text-muted-foreground" href="mailto:xxxinsxxx@qq.com">xxxinsxxx@qq.com</a>
              </div>
            </div>
          </Card>

          <!-- 音乐播放器 -->
          <Card>
            <CardHeader>
              <CardTitle>{{ $t('home.nowPlaying') }}</CardTitle>
            </CardHeader>
            <CardContent>
              <MusicWidget />
            </CardContent>
          </Card>

          <!-- 社交媒体和图片 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Card>
              <CardContent class="p-4">
                <div class="flex flex-col space-y-2">
                  <a href="https://github.com/yourusername" target="_blank">
                    <Button variant="ghost" class="w-full justify-start">
                      <Github class="w-5 h-5 mr-2" />
                      Github
                    </Button>
                  </a>
                  <a href="https://twitter.com/yourusername" target="_blank">
                    <Button variant="ghost" class="w-full justify-start">
                      <Twitter class="w-5 h-5 mr-2" />
                      Twitter
                    </Button>
                  </a>
                </div>
              </CardContent>
            </Card>
            <Card class="hidden sm:block">
              <CardContent class="p-0">
                <img src="/assets/images/IMG_0055.png" alt="Placeholder" class="w-full h-32 object-cover rounded-lg" />
              </CardContent>
            </Card>
          </div>
        </div>

        <!-- 中间栏 -->
        <div class="md:col-span-4 lg:col-span-4 flex flex-col gap-4">
          <!-- 功能导航 -->
          <div class="grid grid-cols-3 gap-4">
            <NuxtLink to="/posts" class="block">
              <Card class="hover:bg-muted/50 transition h-full">
                <CardContent class="p-4 text-center">
                  <FileText class="w-6 h-6 mx-auto mb-2" />
                  <span>{{ $t('nav.posts') }}</span>
                </CardContent>
              </Card>
            </NuxtLink>
            <NuxtLink to="/movies" class="block">
              <Card class="hover:bg-muted/50 transition h-full">
                <CardContent class="p-4 text-center">
                  <Film class="w-6 h-6 mx-auto mb-2" />
                  <span>{{ $t('nav.movies') }}</span>
                </CardContent>
              </Card>
            </NuxtLink>
            <Card class="hover:bg-muted/50 transition h-full">
              <CardContent class="p-4 text-center">
                <Plus class="w-6 h-6 mx-auto mb-2" />
                <span>{{ $t('nav.more') }}</span>
              </CardContent>
            </Card>
          </div>

          <!-- 文字内容 -->
          <Card class="flex-grow ">
            <CardContent class="p-4 overflow-hidden h-full text-muted-foreground text-2xl whitespace-nowrap text-center md:text-left md:flex md:flex-col md:justify-between select-none">
<!--              <div class=" h-full ">-->
<!--                <div class=" ">-->
                  <p class="justify-between flex"><span>有一段时间</span><span>我们仰卧河底，</span></p><br/>
                  <p class="justify-between flex"><span>在另一个角度看</span><span>时光流淌。</span></p><br/>
                  <p class="justify-between flex"><span>你将</span><span>所有的远方称为<span class="highlight" data-text="河流。" >河流。</span></span></p>
<!--                </div>-->
<!--              </div>-->

            </CardContent>
          </Card>

          <!-- 底部图片 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
<!--            <Card class=" bg-gradient-to-br from-[#027fff] from-50% to-[#4eeec2] to-125% h-48">-->
<!--              <CardContent  class="p-4 flex justify-center items-center h-full">-->
<!--                <img src="/assets/images/mario.png" alt="mario" class="w-16 h-16" />-->
<!--              </CardContent>-->
<!--            </Card>-->
          <TiltedCard
              useGradientBackground
              gradientBackground="linear-gradient(45deg, #027fff 50%, #4eeec2 125%)"
              displayOverlayContent
              container-height="192px"
              image-height="192px"
              image-width="192px"
            >
              <template #overlayContent>
                <img src="/assets/images/mario.png" alt="mario" class="w-16 h-16" />
              </template>
            </TiltedCard>
            <TiltedCard
                useGradientBackground
                gradientBackground="linear-gradient(45deg, #14B1A1 10%, #6EEFC2 125%)"
                displayOverlayContent
                container-height="192px"
                image-height="192px"
                image-width="192px"
            >
              <template #overlayContent>
                <img src="/assets/images/poke-ball.png" alt="poke-ball" class="w-16 h-16" />
              </template>
            </TiltedCard>
<!--            <Card class="hidden sm:block bg-gradient-to-br from-[#14B1A1] from-10% to-[#6EEFC2] h-48">-->
<!--              <CardContent class="p-4 flex justify-center items-center  h-full">-->
<!--                <img src="/assets/images/poke-ball.png" alt="poke-ball" class="w-16 h-16" />-->
<!--              </CardContent>-->
<!--            </Card>-->
          </div>
        </div>

        <!-- 右侧栏 -->
        <div class="md:col-span-8 lg:col-span-4 lg:row-span-2 space-y-4">
          <!-- 电影滚动封面 -->
          <Card>
            <CardHeader>
              <CardTitle>{{ $t('home.featuredMovies') }}</CardTitle>
            </CardHeader>
            <CardContent>
              <MovieSlider :movies="movies" />
            </CardContent>
          </Card>

          <!-- 其他内容卡片 -->
          <Card>
            <CardHeader>
              <CardTitle>{{ $t('home.recentActivity') }}</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-4">
                <div class="flex items-center space-x-4">
<!--                  <div class="w-12 h-12 bg-muted rounded-full"></div>-->
                  <div>
                    <h4 class="font-medium">Wait More...</h4>
                    <p class="text-sm text-muted-foreground"></p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <!-- 占位图片 -->
          <Card class="hidden md:block">
            <CardContent class="p-0">
              <img src="/assets/images/IMG_0021.png" alt="Placeholder" class="w-full object-cover rounded-lg aspect-square" />
            </CardContent>
          </Card>
        </div>

        <!-- 最新文章 -->
        <div class="md:col-span-8 lg:col-span-8 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>{{ $t('home.latestPosts') }}</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-4">
                <NuxtLink
                  v-for="post in posts"
                  :key="post._path"
                  :to="post._path"
                  class="block p-4 rounded-lg hover:bg-muted/50 transition"
                >
                  <h3 class="text-xl font-semibold">{{ post.title }}</h3>
                  <div class="flex flex-wrap gap-4 mt-2 mb-3 text-sm text-muted-foreground">
                    <time class="flex items-center">
                      <CalendarIcon class="w-4 h-4 mr-2" />
                      {{ formatDate(post.date) }}
                    </time>
                    <div class="flex flex-wrap items-center gap-2">
                      <NuxtLink
                        v-for="tag in post.tags"
                        :key="tag"
                        :to="`/posts?tag=${tag}`"
                        class="hover:text-primary"
                        @click.stop
                      >
                        #{{ tag }}
                      </NuxtLink>
                    </div>
                  </div>
                  <p class="text-muted-foreground line-clamp-2">{{ post.description }}</p>
                </NuxtLink>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>

    <!-- 添加 Footer -->
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Github, Twitter, FileText, Film, Plus, Calendar as CalendarIcon } from 'lucide-vue-next'
import movieData from '@/data/top-movies.json'
import Footer from '@/components/Footer.vue'
import TiltedCard from "~/components/ReactBitComponents/TiltedCard.vue";

// 使用精选电影列表
const movies = ref(movieData.movies)

// 获取最新文章
const { data: posts } = await useAsyncData('posts', () =>
  queryContent('posts')
    .sort({ date: -1 }) // 按日期降序
    .limit(3) // 只显示最新的3篇
    .find()
)

// 格式化日期
function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 确保首页加载时隐藏悬浮播放器
onMounted(async () => {
  const player = usePlayerStore()
  player.setShowFloating(false)
})
</script>
<style scoped lang="scss" >
.highlight{
  display: inline-block;
  position: relative;
  z-index: 0;
  &:before{
    content: "";
    background-image: linear-gradient(#a1d8f2, #a1d8f2);
    background-repeat: no-repeat;
    background-position: 0;
    background-size: 100% 100%;
    height: 0.5em;
    left: -0.125em;
    bottom:0;
    z-index: -1;
    border-radius: 9px;
    padding-inline: .125em;
    //transform: translateY(-50%);
    width: 100%;
    opacity: 1;
    position: absolute;
    transition: width 0.5s ease-out, opacity .2s ease;
    transition-delay: calc(0.5s* 0);
    animation: animate 1s;
  }
  &:after{
    content: attr(data-text);
    top: 0;
    left: 0;
    overflow: hidden;
    white-space: nowrap;
    color: #2a7af5;
    width: 100%;
    opacity: 1;
    position: absolute;
    transition: width 0.5s ease-out, opacity .2s ease;
    transition-delay: calc(0.5s* 0);
    animation: animate 1s;
  }
  @keyframes animate {
    from {
      //transform: translate(-50%, -50%) scale(0);
      width: 0;
      opacity: 0;
    }
    to {
      //transform: translate(-50%, -50%) scale(1);
      width: 100%;
      opacity: 1;
    }
  }
}
</style>
