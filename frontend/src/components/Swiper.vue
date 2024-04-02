<template>
  <div>
    <h2>Dog Image Generator</h2>
    <input type="text" v-model="userInput" placeholder="Enter a number (1-8)" />
    <button @click="generateDogImages">Generate</button>

    <swiper ref="mySwiper" :modules="modules" :pagination="{ clickable: true }">
      <!-- 动态生成 swiper-slide 组件 -->
      <swiper-slide v-for="(image, index) in dogImages" :key="index">
        <img :src="image" :alt="'Dog Image ' + index">
      </swiper-slide>

      <!-- Add Pagination -->
      <div class="swiper-pagination" slot="pagination"></div>

      <!-- 导航按钮 -->
      <div class="swiper-button-prev" slot="button-prev" @click="swiperPrev"></div>
      <div class="swiper-button-next" slot="button-next" @click="swiperNext"></div>
    </swiper>
  </div>
</template>

<script>

import { Swiper, SwiperSlide } from 'swiper/vue';
import { Navigation, Pagination, Scrollbar, A11y } from 'swiper/modules';


// Import Swiper styles
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';
import 'swiper/css/scrollbar';

export default {
  data() {
    return {
      modules: [Pagination, Navigation], // 添加 Navigation 模块
      dogImages: ["../assets/logo1.png", "../assets/logo.png"], // 示例图片路径
      userInput: '', // 用户输入，可能用于未来功能拓展，如动态加载图片等
    };
  },
  components: {
    Swiper,
    SwiperSlide,
  },
  methods: {
    swiperNext() {
      this.$refs.mySwiper.swiper.slideNext();
    },
    swiperPrev() {
      this.$refs.mySwiper.swiper.slidePrev();
    },
    generateDogImages() {
      // 这里可以添加逻辑来根据 userInput 更新 dogImages 数组，例如通过 API 请求获取图片等。
      // 示例代码中，此方法留空。
    },
  },
};
</script>