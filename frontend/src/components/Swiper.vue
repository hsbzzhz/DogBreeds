<template>
  <div>
    <h2> Dog Image Generator </h2>
    <input type="text" v-model="userInput" placeholder="Enter a number (1-8)"/>
    <button @click="generateDogImages">Generate</button>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <swiper v-if="!errorMessage" ref="mySwiper" :modules="modules" navigation :pagination="{ clickable:true }">
      <swiper-slide v-for="(image, index) in dogImages" :key="index">
        <img :src="image" :alt="index">
      </swiper-slide>

      <!-- Add Pagination -->
      <div class="swiper-pagination" slot="pagination"></div>
      <div class="swiper-bottom">Dog breeds</div>
    </swiper>


    <div class="chat-history" v-if="chatHistory.length > 0">
      <h3>Chat History</h3>
      <ul>
        <li v-for="(message, index) in chatHistory" :key="index">
          <span class="status-light" :class="{'status-green': message.status === 200, 'status-red': message.status !== 200}"></span>
          <span class="execution-time">{{new Date(parseInt(message.execution_time)).toLocaleString() }}</span>

<!--          {{message.status}} {{message.execution_time}} {{ message.input }}-->
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import {Pagination, Navigation} from 'swiper';
// Import Swiper Vue.js components
import {Swiper, SwiperSlide} from 'swiper/vue';

// Import Swiper styles
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

export default {
  data() {
    return {
      modules: [Pagination, Navigation],
      dogImages: ["https://images.dog.ceo/breeds/coonhound/n02089078_2106.jpg",
        "https://images.dog.ceo/breeds/retriever-flatcoated/n02099267_3494.jpg"],
      chatHistory: [],
      userInput: '',
      errorMessage: '',
    }
  },
  created() {
    this.fetchChatHistory();
  },
  components: {
    Swiper,
    SwiperSlide
  },
  methods: {
    async generateDogImages() {
      this.errorMessage = '';
      const inputNumber = parseInt(this.userInput, 10);
      if (isNaN(inputNumber) || inputNumber < 1 || inputNumber > 8) {
        this.errorMessage = '请输入 1 到 8 之间的整数';
      }
      const res = await this.$axios.get(`http://127.0.0.1:5001/api/get-images`, {
        params: {
          number: inputNumber,
          startTime: Date.now()
        }
      })
      if (res.data.status !== 200) {
        this.errorMessage = res.data.message
      } else {
        this.dogImages = res.data.message
      }

      //  更新 history
      this.chatHistory.unshift(res.data)
      console.log(this.chatHistory)
    },
    async fetchChatHistory() {
      const res = await this.$axios.get('http://127.0.0.1:5001/api/get-records');
      if (res.data.status === 200) {
        this.chatHistory = res.data.message;
      }
    }
    },
}
</script>


<style scoped>

.swiper-container {
  /*width: 100%;*/
  /*height: 100%;*/
}

.swiper-slide img {
  /*width: 100%;*/
  /*height: 100%;*/
  /*object-fit: cover;*/
}

.swiper-button-next,
.swiper-button-prev {
  color: #fff; /* Adjust arrow colors as needed */
}

.swiper-bottom {
  top: 200px;
  font-size: 24px;
}
</style>
