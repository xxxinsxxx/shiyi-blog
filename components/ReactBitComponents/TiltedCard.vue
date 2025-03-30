<template>
  <figure
    ref="cardRef"
    class="relative w-full h-full flex flex-col items-center justify-center"
    :style="{
      height: containerHeight,
      width: containerWidth,
      perspective: perspectiveValue
    }"
    @mousemove="handleMouse"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <div
      v-if="showMobileWarning"
      class="absolute top-4 text-center text-sm block sm:hidden"
    >
      This effect is not optimized for mobile. Check on desktop.
    </div>

    <div
      class="relative"
      :style="{
        width: imageWidth,
        height: imageHeight,
        transform: `rotateX(${rotateXValue}deg) rotateY(${rotateYValue}deg) scale(${scaleValue})`,
        transformStyle: 'preserve-3d',
        transition: 'transform 0.1s ease-out'
      }"
    >
      <!-- 使用图片或渐变背景 -->
      <img
        v-if="!useGradientBackground"
        :src="imageSrc"
        :alt="altText"
        class="absolute top-0 left-0 object-cover rounded-[15px] will-change-transform"
        :style="{
          width: imageWidth,
          height: imageHeight,
          transform: 'translateZ(0)'
        }"
      />

      <!-- 渐变背景 -->
      <div
        v-else
        class="absolute top-0 left-0 rounded-[15px] will-change-transform"
        :style="{
          width: imageWidth,
          height: imageHeight,
          background: gradientBackground,
          transform: 'translateZ(0)'
        }"
      ></div>

      <!-- 覆盖内容 -->
      <div
        v-if="displayOverlayContent"
        class="absolute top-0 left-0 w-full h-full z-[2] will-change-transform rounded-[15px] flex items-center justify-center"
        :style="{
          transform: 'translateZ(30px)'
        }"
      >
        <slot name="overlayContent"></slot>
      </div>
    </div>

<!--    <div-->
<!--      v-if="showTooltip"-->
<!--      class="pointer-events-none absolute rounded-[4px] bg-white px-[10px] py-[4px] text-[10px] text-[#2d2d2d] hidden sm:block"-->
<!--      :style="{-->
<!--        left: `${tooltipX}px`,-->
<!--        top: `${tooltipY}px`,-->
<!--        opacity: tooltipOpacity,-->
<!--        transform: `rotate(${rotateFigcaptionValue}deg)`,-->
<!--        transition: 'opacity 0.2s ease-out'-->
<!--      }"-->
<!--    >-->
<!--      {{ captionText }}-->
<!--    </div>-->
  </figure>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';

interface TiltedCardProps {
  imageSrc?: string;
  altText?: string;
  captionText?: string;
  containerHeight?: string;
  containerWidth?: string;
  imageHeight?: string;
  imageWidth?: string;
  scaleOnHover?: number;
  rotateAmplitude?: number;
  showMobileWarning?: boolean;
  showTooltip?: boolean;
  overlayContent?: any;
  displayOverlayContent?: boolean;
  useGradientBackground?: boolean;
  gradientBackground?: string;
  perspectiveRatio?: number; // 新增透视比例属性
}

const props = withDefaults(defineProps<TiltedCardProps>(), {
  imageSrc: "/assets/images/IMG_0021.png",
  altText: "Tilted card image",
  captionText: "",
  containerHeight: "300px",
  containerWidth: "100%",
  imageHeight: "300px",
  imageWidth: "300px",
  scaleOnHover: 1,
  rotateAmplitude: 14,
  showMobileWarning: true,
  showTooltip: true,
  overlayContent: null,
  displayOverlayContent: false,
  useGradientBackground: false,
  gradientBackground: "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)",
  perspectiveRatio: 3 // 默认透视比例
});

const cardRef = ref<HTMLElement | null>(null);
const rotateXValue = ref(0);
const rotateYValue = ref(0);
const scaleValue = ref(1);
const tooltipX = ref(0);
const tooltipY = ref(0);
const tooltipOpacity = ref(0);
const rotateFigcaptionValue = ref(0);
const lastY = ref(0);

// 使用 spring 效果的简化版本
const applySpringEffect = (target: any, value: number, damping = 0.1) => {
  const currentValue = target.value;
  target.value = currentValue + (value - currentValue) * damping;
};

// 处理鼠标移动
const handleMouse = (e: MouseEvent) => {
  if (!cardRef.value) return;

  const rect = cardRef.value.getBoundingClientRect();
  const offsetX = e.clientX - rect.left - rect.width / 2;
  const offsetY = e.clientY - rect.top - rect.height / 2;

  const rotationX = (offsetY / (rect.height / 2)) * -props.rotateAmplitude;
  const rotationY = (offsetX / (rect.width / 2)) * props.rotateAmplitude;

  // 应用平滑过渡效果
  rotateXValue.value = rotationX;
  rotateYValue.value = rotationY;

  tooltipX.value = e.clientX - rect.left;
  tooltipY.value = e.clientY - rect.top;

  const velocityY = offsetY - lastY.value;
  rotateFigcaptionValue.value = -velocityY * 0.6;
  lastY.value = offsetY;
};

// 处理鼠标进入
const handleMouseEnter = () => {
  scaleValue.value = props.scaleOnHover;
  tooltipOpacity.value = 1;
};

// 处理鼠标离开
const handleMouseLeave = () => {
  tooltipOpacity.value = 0;
  scaleValue.value = 1;
  rotateXValue.value = 0;
  rotateYValue.value = 0;
  rotateFigcaptionValue.value = 0;
};

// 计算透视值
const perspectiveValue = computed(() => {
  // 从containerHeight中提取数值部分
  const heightMatch = String(props.containerHeight).match(/(\d+)/);
  const heightValue = heightMatch ? parseInt(heightMatch[0]) : 300;

  // 透视值 = 容器高度 * 透视比例
  return `${heightValue * props.perspectiveRatio}px`;
});
</script>

<style scoped>
/* 可以添加额外的样式 */
</style>
