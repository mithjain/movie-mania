<template>
  <div id="app">
    <dashboard />
  </div>
</template>

<script>

  import Dashboard from '@/components/Dashboard.vue';

  export default {
    components: { Dashboard },
    data: function () {
      return {
        loadingScreen: false,
      };
    },
  };
</script>

<style scoped>
</style>
