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
          <span class="input">{{ message.input }}</span>
          <span class="status-light"
                :class="{'status-green': message.status === 200, 'status-red': message.status !== 200}"></span>
          <span class="execution-time">{{ new Date(parseInt(message.execution_time)).toLocaleString() }}</span>
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
      dogImages: [],
      chatHistory: [],
      userInput: '',
      errorMessage: '',
    }
  },
  mounted() {
    this.fetchChatHistory();
  },
  components: {
    Swiper,
    SwiperSlide
  },
  methods: {
    generateDogImages() {
      this.errorMessage = '';
      const inputNumber = parseInt(this.userInput, 10);
      if (isNaN(inputNumber) || inputNumber < 1 || inputNumber > 8) {
        this.errorMessage = '请输入 1 到 8 之间的整数';
      }
      this.$axios.get(`http://127.0.0.1:5001/api/get-images`, {
        params: {
          number: inputNumber,
          startTime: Date.now()
        }
      }).then(res => {
        if (res.data.status !== 200) {
          this.errorMessage = res.data.message
        } else {
          this.dogImages = res.data.message
        }

        //  更新 history
        this.chatHistory.unshift(res.data)
      })
    },
    fetchChatHistory() {
      this.$axios.get('http://127.0.0.1:5001/api/get-records')
          .then(response => {
            this.chatHistory = response.data.message;
          });
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

.chat-history {
  margin-bottom: 20px; /* 根据需要调整间距 */
}

.chat-history ul {
  list-style: none;
  padding: 0;
}

.chat-history li {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-history .status-light {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 10px;
}

.chat-history .status-green {
  background-color: green;
}

.chat-history .status-red {
  background-color: red;
}

.chat-history .message-content {
  flex-grow: 1;
}

.chat-history .execution-time {
  color: #888;
}
</style>
