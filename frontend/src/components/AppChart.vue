<template>
  <vs-row
    vs-w="12"
    vs-type="flex"
  >
    <vs-col
      class="flex-box flex-wrap"
      vs-justify="center"
      vs-type="flex"
      vs-w="12"
    >
      <chart
        ref="echarts"
        :auto-resize="true"
        :options="chart"
        :style="graphSize"
      />
    </vs-col>
  </vs-row>
</template>

<script>

  import Chart from 'vue-echarts';

  export default {
    name: 'AppChart',
    components: { Chart },
    props: {
      chart: {
        type: Object,
        default: null
      },

    },
    data () {
      return {
        'graphSize': {
          'width': null,
          'height': null,
        }
      };
    },
    mounted () {
      this.updateGraphSize();
    },
    methods: {
      updateGraphSize: function () {
        this.$nextTick(() => {
          let width = window.innerWidth;
          let height;
          if (width > 1000) {
            width = width - 30;
          }
          if (width > 800) {
            height = width * 0.3;
            width = width - 110;
          } else if (width > 500) {
            height = width * 0.4;
            width = width - 95;
          } else {
            height = width * 0.6;
            width = width - 95;
          }
          this.graphSize = {
            'width': `${ width }px`,
            'height': `${ height }px`,
          };
        });
      }
    }
  };

</script>

<style scoped>

</style>