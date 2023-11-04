<template>
  <div
    id="navbar"
    class="navbar-container"
    :class="'z-level-6 position-relative'"
  >
    <vs-row class="text-align-center mt-25">
      <span
        style="font-weight: bolder;font-size: 22px;"
      >
        MOVIE MANIA
      </span>
    </vs-row>
  </div>
</template>

<script>

  export default {
    name: 'NavBar',
  };
</script>


<style lang="scss">
  .profile-menu-container {
    .vs-dropdown--menu {
      margin-right: 7px;
    }
  }

</style>

<style scoped lang="scss">
  .navbar-container {
    width: 100%;
    max-height: 60px;
    overflow-y: hidden;
    overflow-x: hidden;
    background-color: #FFFFFF;


    .navbar {
      .logo-container {
        height: 60px;

        .logo {
          width: 180px;
        }
      }

      .content-container {
        background: #F5F8F6 !important;
        height: 60px;
      }
    }
  }
</style>
