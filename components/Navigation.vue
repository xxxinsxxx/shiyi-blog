<template>
  <nav>
    <NuxtLink to="/">{{ $t('nav.home') }}</NuxtLink>
    <NuxtLink to="/posts">{{ $t('nav.posts') }}</NuxtLink>
    <NuxtLink to="/movies">{{ $t('nav.movies') }}</NuxtLink>
    
    <!-- 语言切换器 -->
    <select v-model="$i18n.locale">
      <option 
        v-for="locale in $i18n.locales" 
        :key="locale.code"
        :value="locale.code"
      >
        {{ locale.name }}
      </option>
    </select>
  </nav>
</template> 