<template>
  <div>
    <h2> Dog Image Generator </h2>
    <input type="text" v-model="userInput" placeholder="Enter a number (1-8)"/>
    <button @click="generateDogImages">Generate</button>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <el-carousel v-if="dogImages.length > 0"
                 :interval="5000" arrow="always" trigger="click">
      <el-carousel-item v-for="(image, index) in dogImages" :key="index">
        <img @click="showFullScreenImage(image)" :src="image" class="carousel-image" :alt="index">
      </el-carousel-item>
    </el-carousel>
    <div v-if="showModal" class="fullscreen-modal" @click="showModal = false">
      <img :src="currentImage" class="fullscreen-image" alt=""/>
    </div>
    <div class="chat-history" v-if="chatHistory.length > 0">
      <h3>Chat History</h3>

      <el-table
          :data="chatHistory"
          style="width: 100%"
          :row-class-name="tableRowClassName">
        <el-table-column
            prop="execution_time"
            label="date"
            width="180">
        </el-table-column>
        <el-table-column
            prop="input"
            label="input"
            width="180">
        </el-table-column>
        <el-table-column
            prop="message"
            label="result">
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      dogImages: [],
      chatHistory: [],
      userInput: '',
      errorMessage: '',
      showModal: false, // 控制模态层的显示
      currentImage: '',
    }
  },
  mounted() {
    this.fetchChatHistory();
  },
  components: {},
  methods: {
    generateDogImages() {
      this.errorMessage = '';
      this.dogImages = [];
      const inputNumber = Number(this.userInput);
      if(!(Number.isInteger(inputNumber) && inputNumber >= 1 && inputNumber <= 8)) {
        this.errorMessage = 'Please enter an integer from 1 to 8';
      }
      this.$axios.get(`http://127.0.0.1:5001/api/get-images`, {
        params: {
          number: this.userInput,
          startTime: Date.now()
        }
      }).then(res => {
        if (res.data.status !== 200) {
          this.errorMessage = res.data.message
        } else {
          this.dogImages = res.data.message
        }

        //  更新 history
        res.data.execution_time = new Date(parseInt(res.data.execution_time)).toLocaleString()
        this.chatHistory.unshift(res.data)
      })
    },
    fetchChatHistory() {
      this.$axios.get('http://127.0.0.1:5001/api/get-records')
          .then(response => {
            const records = response.data.message;
            if (records.length > 0) {
              records.forEach(item => {
                item.execution_time = new Date(parseInt(item.execution_time)).toLocaleString()
              })
            }
            this.chatHistory = records
          });
    },
    showFullScreenImage(image) {
      this.currentImage = image;
      this.showModal = true;
    },
    tableRowClassName({row, rowIndex}) {
      if (row.status !== 200) {
        return 'warning-row';
      }
      return 'success-row';

    }
  },
}
</script>


<style scoped>
.el-carousel__item h3 {
  color: #475669;
  font-size: 18px;
  opacity: 0.75;
  line-height: 300px;
  margin: 0;
}

.carousel-image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.fullscreen-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7); /* 背景模糊效果 */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999; /* 确保模态层在最上层 */
}

.fullscreen-image {
  max-width: 90%;
  max-height: 90%;
}

.el-table .warning-row {
  background: #ee8699;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>
