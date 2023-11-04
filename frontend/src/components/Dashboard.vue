<template>
  <div
    class="main-container overflow-auto"
  >
    <loading-window
      v-if="loadingScreen.length"
      :message="loadingScreen[0]['message']"
    />
    <vs-row>
      <nav-bar
        class="navbar"
      />
    </vs-row>
    <div
      class="body-container"
    >
      <vs-row
        vs-type="flex"
        vs-justify="flex-start"
        class="background-white m-auto"
        style="padding-bottom: 10px;"
      >
        <vs-col
          v-for="filter in filters"
          :key="filter.name"
          vs-w="3"
          class="parent-container p-10"
          vs-type="flex"
          vs-align="center"
        >
          <multi-select
            v-model="filter.selected_values"
            :multiple="true"
            placeholder=""
            :label="filter.label"
            :allow-all-selection="true"
            required="true"
            class="db-form-input"
            style="padding: 0.2rem; width:400px !important;"
          >
            <multi-select-item
              v-for="value in filter.options"
              :key="value"
              :value="value"
              :text="value"
            />
          </multi-select>
        </vs-col>
        <vs-col
          vs-w="2"
          vs-type="flex"
          vs-align="flex-end"
          vs-justify="center"
        >
          <vs-button
            :color="'blue'"
            size="small"
            class="mr-15"
            @click="applyFilters()"
          >
            Apply
          </vs-button>
          <vs-button
            class="ml-5"
            :color="'lightgrey'"
            size="small"
            @click="resetFilters()"
          >
            Reset
          </vs-button>
        </vs-col>
      </vs-row>
      <vs-row
        vs-w="11.5"
        class="pt-20"
      >
        <vs-col
          vs-offset="0.5"
          vs-type="flex"
          vs-align="center"
          vs-w="12"
        >
          <vs-card class="pt-20 text-align-center">
            <h1>
              Total Number of Movies: 234
            </h1>
          </vs-card>
        </vs-col>
      </vs-row>
      <vs-row
        vs-w="11.5"
        class="pt-20"
      >
        <vs-col
          vs-offset="0.5"
          vs-type="flex"
          vs-align="center"
          vs-w="12"
        >
          <vs-card class="pt-20 text-align-center">
            <h1>
              Total Number of Movies: 234
            </h1>
          </vs-card>
        </vs-col>
      </vs-row>
      <vs-row
        vs-w="11.5"
        class="pt-20"
      >
        <vs-col
          vs-offset="0.5"
          vs-type="flex"
          vs-align="center"
          vs-w="12"
        >
          <vs-card class="pt-20 text-align-center">
            <h1>
              Total Number of Movies: 234
            </h1>
          </vs-card>
        </vs-col>
      </vs-row>
    </div>
  </div>
</template>

<script>
  import NavBar from './navbar/NavBar';
  import MultiSelectItem from '@/components/inputs/MultiSelectItem.vue';
  import MultiSelect from '@/components/inputs/MultiSelect.vue';
  import LoadingWindow from '@/components/helpers/LoadingWindow.vue';


  export default {
    components: {
      NavBar,
      MultiSelectItem,
      MultiSelect,
      LoadingWindow
    },
    data: function () {
      return {
        filters: [
          { 'name': 'genre', 'label': 'Genre', 'options': [], 'selected_values': [] },
          { 'name': 'directors', 'label': 'Directors', 'options': [], 'selected_values': [] },
          { 'name': 'actors', 'label': 'Actors', 'options': [], 'selected_values': [] },
        ],
        loadingScreen: [],
      };
    },
    beforeMount () {
      // this.getFilterOptions();
    },
    methods: {
      getFilterOptions: function () {
        this.axiosPromise({
          url: '/movies/filters/',
          method: 'GET',
        }).then(response => {
          this.filters.forEach((filter) => {
            filter.options = response[filter.name];
          });
        });
      },
      applyFilters: function () {

      },
      resetFilters: function () {
        this.filters.forEach((filter) => {
          filter.selected_values = [];
        });
      },

    }
  };
</script>

<style lang="scss" scoped>
  .fixParent {
    z-index: auto !important;
    opacity: 1.0 !important;
    position: absolute !important;
  }

  .navbar {
    height: 60px;
  }

  .sub-navbar {
    max-height: 45px;
    overflow-y: hidden;
  }

  .fadeIn {
    animation-duration: 0.2s;
  }

  .main-routes {
    height: calc(125vh - 105px);
  }

  .parent-container {
    bottom: 0;
    left: 0;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    width: 16.6%;
  }


  .main-container {
    background-color:  #f0f5f5;
;
    //min-height: 5000px;
  }

  .commentary-container {
    min-height: 300px;
  }

  .body-container {
    height: 120vh;
  }
</style>