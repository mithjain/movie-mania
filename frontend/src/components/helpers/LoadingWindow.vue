<template>
  <div
    :class="'loadingWindowOlder z-level-7 ' + (fullPage ? 'fullpage-loader' : 'component-loader')"
  >
    <div style="display: flex;align-items: center;flex-direction: column">
      <div
        class="half-circle-spinner"
      >
        <div class="circle circle-1" />
        <div class="circle circle-2" />
      </div>
      <div>
        <div
          v-if="message"
          class="loading-message"
        >
          {{ message }}
        </div>
        <div
          v-if="uploadProgress"
        >
          <div
            style="margin-left: 1.45vw;color: rgba(var(--vs-primary), 1);size: 20px;horiz-align: center"
          >
            {{ uploadProgress }}%
          </div>
          <div
            style="margin-left: 0.05vw;color: rgba(var(--vs-primary), 1);size: 10px"
          >
            uploaded
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>

  export default {
    props: {
      message: {
        type: String,
        default: null,
      },
      fullPage: {
        type: Boolean,
        default: false,
      },
      uploadProgress: {
        type: Number,
        default: undefined
      }

    },
  };
</script>
<style lang="scss" scoped>
  .loading-message {
    color: rgba(var(--vs-primary), 1);
    size: 20px;
    text-align: center
  }

  .fullpage-loader {
    position: fixed;
  }

  .component-loader {
    position: absolute;
  }

  .loadingWindowOlder {
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .half-circle-spinner, .half-circle-spinner * {
    box-sizing: border-box;
  }

  .half-circle-spinner {
    width: 5vw;
    height: 5vw;
    border-radius: 100%;
    position: relative;
  }

  .half-circle-spinner .circle {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 100%;
    border: calc(60px / 10) solid transparent;
  }

  .half-circle-spinner .circle.circle-1 {
    border-top-color: rgba(var(--vs-primary), 1);
    animation: half-circle-spinner-animation 1s infinite;
  }

  .half-circle-spinner .circle.circle-2 {
    border-bottom-color: rgba(var(--vs-primary), 1);
    animation: half-circle-spinner-animation 1s infinite alternate;
  }

  @keyframes half-circle-spinner-animation {
    0% {
      transform: rotate(0deg);

    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
