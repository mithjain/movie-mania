<template>
  <div
    v-if="isShow"
    :class="[
      disabled ? 'text-disabled' : '',
      activeMultiSelectItemIndex===myIndex?'active-item':''
    ]"
    class="pointer-cursor select-item-container"
    @click="selectOption"
  >
    <slot>
      <div
        :id="testingId"
        :class="[selected ? mode === 'report-filter' ? '' : 'selected-item' : '',
                 mode === 'report-filter' ? 'report-filter' : '']"
        :title="tooltip || text"
        class="default-content pl-10 pr-5 mt-5"
      >
        <div
          v-if="mode === 'report-filter'"
          :class="selected ? 'filled' : ''"
          class="radio mr-10"
        />
        <span class="select-item-text">
          <slot
            name="icon"
          >
            <i
              :class="icon"
              class="pr-5"
            />
          </slot>
          <span
            v-html="text"
          />
        </span>
        <i
          v-if="selected && mode === 'default'"
          class="fas fa-check font-smaller pr-5"
        />
      </div>
    </slot>
  </div>
</template>
<script>
  export default {
    name: 'MultiSelectItem',
    props: {
      text: {
        type: [String, Number],
        default: null
      },
      value: {
        type: [String, Number, Object, Array],
        default: null
      },
      disabled: {
        type: Boolean,
        default: false
      },
      icon: {
        type: String,
        default: null
      },
      mode: {
        type: String,
        default: 'default',
      },
      testingId: {
        type: String,
        default: null,
      },
      isSelected: {
        type: Boolean,
        default: false,
      },
      tooltip: {
        type: String,
        default: null
      }
    },
    data: function () {
      return {};
    },

    computed: {
      selected: function () {
        if (this.isSelected) return true;
        let selected = false;
        let multiselect = this.getMultiSelect();
        let multiselectProps = multiselect.$props;
        let multiselectValues = multiselectProps.value;
        if (multiselectProps['multiple']) {
          if (multiselectValues) {
            if (multiselectValues.indexOf(this.value) !== -1) {
              selected = true;
            }
          }
        } else {
          if (multiselectValues === this.value) {
            selected = true;
          }
        }
        return selected;
      },
      searchKeyword: function () {
        return this.getMultiSelect().$data['searchKeyword'];
      },
      isShow: function () {
        if (! this.text && this.text !== 0)
          return false;
        if (this.getMultiSelect().autoComplete) {
          if (this.searchKeyword.length > 0) {
            return this.text.toString().toLowerCase().includes(this.searchKeyword.toLowerCase());
          } else {
            return true;
          }
        } else return true;
      },
      activeMultiSelectItemIndex: function () {
        return this.getMultiSelect().activeMultiSelectItemIndex;
      },
      myIndex: function () {
        return this.getMultiSelect().getChildren().indexOf(this);
      },
    },
    watch: {},
    mounted: function () {
      this.getMultiSelect().updateSelectedText();
    },
    methods: {
      getMultiSelect: function () {
        return this.getParentComponentByName(this, 'MultiSelect');
      },
      selectOption: function () {
        if (! this.disabled) {
          let action = this.selected ? 'remove' : 'add';
          this.getMultiSelect().selectOption(this.value, this.text, action);
          this.$emit('changed', action, this.value);
        }
      },
    }
  };
</script>

<style lang="scss" scoped>
  .select-item-container {
    border-radius: 2px;
    transition: all 0.25s ease-in-out;

    &.active-item {
      background: #e7e5e5;
    }

    .default-content {
      display: flex;
      margin: 0 5px;
      align-items: center;
      justify-content: space-between;
      padding: 5px;
      border-radius: 5px;

      &.report-filter {
        justify-content: flex-start;
      }

      &:hover {
        .select-item-text {
          margin-left: 5px;
        }

        color: rgba(var(--vs-primary), 1);
        background-color: rgba(var(--vs-secondary), 0.025);
      }

      .select-item-text {
        transition: all 0.2s ease;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }

    .radio {
      min-width: 13px;
      height: 13px;
      border-radius: 50%;
      border: 1px solid grey;

      &.filled {
        background-color: rgba(var(--vs-primary), 1);
      }
    }

    .selected-item {
      color: rgba(var(--vs-primary), 1);
      background-color: rgba(var(--vs-secondary), 0.075);
    }
  }
</style>