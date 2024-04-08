<template>
  <div>
    <h2> Dog Image Generator </h2>
    <el-space>
      <el-input class="input-search" type="text" v-model="userInput" placeholder="Enter a number (1-8)"/>
      <el-button type="primary" @click="generateDogImages">Generate</el-button>
    </el-space>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <el-carousel class="mt16" v-if="dogImages.length > 0"
                 @change="updateCurrentBreed"
                 :interval="5000"
                 arrow="always"
                 trigger="click">
      <el-carousel-item v-for="(image, index) in dogImages" :key="index">
        <img @click="showFullScreenImage(image)" :src="image" class="carousel-image" :alt="index">
      </el-carousel-item>
    </el-carousel>

    <div v-if="dogImages.length > 0">
      <h4>{{ currentBreed }}</h4>
    </div>
    <div v-if="showModal" class="fullscreen-modal" @click="showModal = false">
      <img :src="currentImage" class="fullscreen-image" alt=""/>
    </div>
    <div class="chat-history" v-if="chatHistory.length > 0">
      <el-divider>
        <h3>Chat History</h3>
      </el-divider>

      <el-table
          size="small"
          :data="chatHistory"
          height="300"
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
      currentBreed: '',
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
      if (!(Number.isInteger(inputNumber) && inputNumber >= 1 && inputNumber <= 8)) {
        this.errorMessage = 'Please introduce any number between 1 and 8'
      }
      this.$axios.get(`/api/get-images`, {
        params: {
          number: this.userInput,
          startTime: Date.now()
        }
      }).then(res => {
        if (res.data.status === 200) {
          this.dogImages = res.data.message
          const breedMatch = this.dogImages[0].match(/breeds\/([^/]+)\//)
          this.currentBreed = breedMatch[1].replace(/-/g, ' ')

        } else if (res.data.status === 500) {
          this.errorMessage = 'Oops, unable to load data, please try again.'
        }

        //  更新 history
        res.data.execution_time = new Date(parseInt(res.data.execution_time)).toLocaleString()
        this.chatHistory.unshift(res.data)
      })
    },
    updateCurrentBreed(index) {
      const imageUrl = this.dogImages[index];
      const breedMatch = imageUrl.match(/breeds\/([^/]+)\//);
      if (breedMatch && breedMatch[1]) {
        this.currentBreed = breedMatch[1].replace(/-/g, ' '); // 替换链接中的'-'为空格以美化品种名称
      } else {
        this.currentBreed = 'Unknown Breed'; // 如果没有匹配到品种，则显示"Unknown Breed"
      }
    },
    fetchChatHistory() {
      this.$axios.get('/api/get-records')
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
.mt16 {
  margin-top: 16px;
}

.input-search {
  width: 250px;
}

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
  object-fit: scale-down;
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

.chat-history {
  margin-top: 64px;
}

.fullscreen-image {
  max-width: 90%;
  max-height: 90%;
}

:deep(.el-table__body tr) {
  pointer-events: none;
}

:deep(.el-table__body tr.warning-row) {
  background: #ee8699;
}

:deep(.el-table__body tr.success-row) {
  background: #f0f9eb;
}
</style>
