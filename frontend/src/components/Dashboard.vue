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
      class="body-container thinScrollbar"
      style="overflow-y: auto;"
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
            size="medium"
            class="mr-15"
            @click="applyFilters()"
          >
            Apply
          </vs-button>
          <vs-button
            class="ml-5"
            :color="'lightgrey'"
            size="medium"
            @click="resetFilters()"
          >
            Reset
          </vs-button>
        </vs-col>
      </vs-row>
      <vs-row>
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
                Total Number of Movies: {{ totalMoviesCount }}
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
              <span>
                Number of Movies released By Year
              </span>
              <app-chart
                :chart="movieByYearChart"
              />
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
              <span>
                Average rating of Movies for each Genre across Years
              </span>
              <app-chart
                :chart="avgRatingByYear"
              />
            </vs-card>
          </vs-col>
        </vs-row>
      </vs-row>
    </div>
  </div>
</template>

<script>
  import NavBar from './NavBar.vue';
  import MultiSelectItem from '@/components/inputs/MultiSelectItem.vue';
  import MultiSelect from '@/components/inputs/MultiSelect.vue';
  import LoadingWindow from '@/components/helpers/LoadingWindow.vue';
  import AppChart from '@/components/AppChart.vue';

  export default {
    components: {
      AppChart,
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
        totalMoviesCount: null,
        movieByYearChart: null,
        avgRatingByYear: null,
      };
    },
    beforeMount () {
      this.loadingScreen.push(true);
      this.getFilterOptions();
      this.applyFilters();
      this.loadingScreen.pop(true);
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
        this.loadingScreen.push(true);
        let requestData = { 'filters': {} };
        this.filters.forEach((filter) => {
          requestData['filters'][filter.name] = filter.selected_values;
        });
        this.axiosPromise({
          url: '/movies/cards/',
          method: 'POST',
          data: requestData
        }).then(response => {
          this.totalMoviesCount = response['total_movies_count'];
          this.movieByYearChart = response['movie_by_year'];
          this.avgRatingByYear = response['avg_rating_by_year'];
          this.loadingScreen.pop(true);
        });
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
    background-color: #f0f5f5;;
    //min-height: 5000px;
  }

  .commentary-container {
    min-height: 300px;
  }

  .body-container {
    height: 120vh;
  }
</style>