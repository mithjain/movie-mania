<template>
  <div
    v-click-outside="closeSelect"
    :class="'multiselect-'+size"
    class="multiselect-container"
  >
    <div
      :class="labelClass"
      class="label-text font-medium flex-box flex-wrap"
    >
      {{ label }}
    </div>
    <div
      ref="select-parent-container"
      :class="[autoComplete?'pr-5':'', mode === 'default'? '' : `input-container-${mode}` ]"
      :style="getSelectParentStyle"
      class="width-100 input-container mt-5"
    >
      <div
        ref="multi-select-selected-text"
        :class="[(showIcon?'':'no-icon'), (mode === 'default'? '' : `search-container-${mode}`)]"
        :style="{'height':`${sizePixelMap[size]}px`}"
        :title="selectedItemsText"
        class="search-container pointer-cursor pl-5 pr-5 break-word"
        @click="toggleSelect()"
      >
        <template
          v-if="(!renderCustomContent) && multiple && tagsEnabled && value"
        >
          <div
            class="width-100 pb-5 flex-box flex-wrap overflow--y-auto thinScrollbar tags-display"
          >
            <template
              v-for="(selectedItem,index) in selectedItems"
            >
              <span
                :key="selectedItem+index"
                class="bg-primary text-white p-5 mr-5 mt-5 border-radius-5 font-small"
                @click.stop="removeSelectedItem(selectedItem,index)"
              >
                {{ selectedItem }}
                <i
                  class="fas fa-times"
                />
              </span>
            </template>
          </div>
        </template>
        <template
          v-else
        >
          <div
            class="width-100 search-input font-medium width-100 ellipsis-word"
            @keydown="handleKeyPress"
          >
            <slot
              name="content"
            >
              <input
                v-show="autoComplete"
                ref="multi-select-input"
                v-model="searchKeyword"
                :class="getSearchContainerClass"
                :disabled="disabled"
                :placeholder="forcePlaceholder || selectedItemsText || placeholder"
                :title="forcePlaceholder || selectedItemsText || placeholder"
                autocomplete="nope"
                class="overflow--both-hidden ellipsis-word width-100 p-10 bordered-none search-input font-medium
              multi-select-input"
                tabindex="-1"
                type="text"
                @keydown.esc="keyPressHandlers['escape']"
              >
            </slot>
          </div>
        </template>
      </div>
      <div
        v-if="showIcon && !disabled"
        :class="mode === 'default'? '' : `icons-container-${mode}`"
        class="icons-container font-smallest text-align-center"
        @click="toggleSelect(true)"
      >
        <div
          v-if="searchKeyword.length>0"
          :class="mode === 'report-filters'
            ?'text-white bg-primary font-medium icon-down-container'
            :'width-50 hover:text-primary'"
          class="pointer-cursor"
          @click.stop="searchKeyword=''"
        >
          <i
            :class="iconClose+' '+iconPack"
          />
        </div>
        <div
          v-else
          :class="mode === 'report-filters'
            ? 'text-white bg-primary font-medium icon-down-container'
            : 'width-50 hover:text-primary'"
          class="pointer-cursor"
        >
          <i
            :class="[iconDecider,iconClass]"
          />
        </div>
      </div>
    </div>
    <template>
      <transition
        enter-active-class="animated fadeIn faster"
        name="custom-classes-transition"
      >
        <div
          v-show="showOptions"
          ref="options-container"
          class="options-container w-100 z-level-6i"
          :style="optionsContainerStyle"
          @click.stop
        >
          <template
            v-if="autoComplete && tagsEnabled"
          >
            <vs-row
              vs-align="center"
            >
              <input
                ref="multi-select-input"
                v-model="searchKeyword"
                :placeholder="placeholder"
                :title="placeholder"
                autocomplete="nope"
                class="overflow--both-hidden ellipsis-word width-85 pv-8 pl-10 bordered-none search-input font-medium
              multi-select-input"
                tabindex="-1"
                type="text"
                @keydown.esc="keyPressHandlers['escape']"
                @keydown.enter="keyPressHandlers['enter']"
              >
              <div
                v-if="searchKeyword.length>0"
                class="width-15 text-align-center hover:text-primary pointer-cursor"
                title="Add this custom value"
                @click="keyPressHandlers['enter']"
              >
                <vs-icon
                  icon="fas fa-plus-square"
                  icon-pack="fa5"
                />
              </div>
            </vs-row>
          </template>
          <div
            v-if="mode === 'report-filter'"
            :class="dropdown === 'bottom'? 'dropdown-bottom' : 'dropdown-top'"
            :style="dropdownInvertedCornerStyle"
            class="inverted-corners"
          />
          <vs-row
            v-if="multiple && allowAllSelection"
            ref="select-all-container"
            :class="disableSelectAll ? 'text-disabled' : ''"
            class="select-all pointer-cursor mt-5"
          >
            <vs-col
              vs-align="center"
              vs-type="flex"
              @click.native="selectAllOptions"
            >
              <div
                v-if="mode === 'report-filter'"
                :class="isSelectAllSelected ? 'filled' : ''"
                class="select-all-selected"
              />
              <p :class="(mode !== 'report-filter' && isSelectAllSelected) ? 'text-primary':''">
                Select All
              </p>
            </vs-col>
          </vs-row>
          <div
            ref="multiselectItemContainer"
            :style="optionsDisplayStyle"
            class="thinScrollbar overflow--x-hidden"
            @click.stop=""
          >
            <slot />
            <div
              v-show="paginatedValue"
              class="text-primary pointer-cursor m-5 p-5 pl-10"
              @click="appendOptions"
            >
              {{ `Show ${ paginatedValue } more` }}
            </div>
          </div>
        </div>
      </transition>
    </template>
  </div>
</template>

<script>
  import { domMixins } from '@/mixins/domMixins';
  import { scrollerMixin } from '@/mixins/scrollerMixin';

  export default {
    name: 'MultiSelect',
    mixins: [domMixins, scrollerMixin],
    props: {
      icon: {
        type: String,
        default: 'fas fa-angle-down'
      },
      iconPack: {
        type: String,
        default: 'fa5'
      },
      iconClose: {
        type: String,
        default: 'fas fa-times'
      },
      label: {
        type: String,
        default: null
      },
      labelPlaceholder: {
        type: String,
        default: () => 'Search'
      },
      placeholder: {
        type: String,
        default: () => 'Search'
      },
      renderCustomContent: {
        type: Boolean,
        default: false,
      },
      multiple: {
        type: Boolean,
        default: false
      },
      autoComplete: {
        type: Boolean,
        default: true
      },
      showIcon: {
        type: Boolean,
        default: true
      },
      value: {
        type: [Array, String, Number, Object],
        default: null,
      },
      disabled: {
        type: Boolean,
        default: false
      },
      min: {
        type: [String, Number],
        default: 0,
      },
      max: {
        type: [String, Number],
        default: -1
      },
      overrideSelectedValues: {
        type: Boolean,
        default: false,
      },
      overridePosition: {
        type: String,
        default: 'start'
      },
      size: {
        type: String,
        default: 'small'
      },
      noBorder: {
        type: Boolean,
        default: false,
      },
      tagsEnabled: {
        type: Boolean,
        default: false,
      },
      allowAllSelection: {
        type: Boolean,
        default: false
      },
      customValueEnabled: {
        type: Boolean,
        default: false,
      },
      message: {
        type: String,
        default: null,
      },
      mode: {
        type: String,
        default: 'default',
      },
      iconSearch: {
        type: String,
        default: 'fas fa-search'
      },
      labelClass: {
        type: [String, Array],
        default: ''
      },
      iconClass: {
        type: String,
        default: '',
      },
      paginatedValue: {
        type: [Number, String],
        default: 0
      },
      forceShowSelectedText: {
        type: Boolean,
        default: false,
      },
      disableSelectAll: {
        type: Boolean,
        default: false
      },
      closeOnToggle: {
        type: Boolean,
        default: true,
      },
      maxContentWidth: {
        type: Boolean,
        default: false,
      },
      forcePlaceholder: {
        type: String,
        default: null
      },
      allowKeyNavigation: {
        type: Boolean,
        default: true
      },
      emitNullOnEmpty: {
        type: Boolean,
        default: false,
      }
    },
    data: function () {
      return {
        isMounted: false,
        isFocused: false,
        focusBorder: { border: '1px solid rgba(var(--vs-primary), 1)', boxShadow: '0 3px 10px 0 rgba(0,0,0,.15)' },
        searchKeyword: '',
        showOptions: false,
        optionsContainerStyle: {},
        values: [],
        listeners_ddd: {
          'open': this.openSelect,
          'close': this.closeSelect,
        },
        keyPressHandlers: {
          'escape': this.handleEscape,
          'enter': this.handleEnter,
        },
        selectedItemsText: null,
        selectedItems: [],
        sizePixelMap: {
          'smaller': 28,
          'small': 35,
          'regular': 42,
          'large': 50
        },
        dropdown: 'bottom',
        isSelectAllSelected: false,
        dropdownInvertedCornerStyle: {},
        activeMultiSelectItemIndex: -1,
      };
    },
    computed: {
      optionContainerWidth: function () {
        if (this.isMounted)
          return this.$refs['select-parent-container'].clientWidth;
        return null;
      },
      parent () {
        return this;
      },
      minimum: function () {
        let minType = typeof this.min;
        if (minType === 'string') {
          let parsedMin = parseInt(this.min);
          if (isNaN(parsedMin)) parsedMin = 0;
          return parsedMin;
        }
        return this.min;
      },
      maximum: function () {
        let maxType = typeof this.max;
        if (maxType === 'string') {
          let parsedMax = parseInt(this.max);
          if (isNaN(parsedMax)) parsedMax = -1;
          return parsedMax;
        }
        return this.max;
      },
      getSelectParentStyle: function () {
        let style = {};
        let boxShadow = null;
        let borderColor = 'lightgray';
        if (this.noBorder) {
          borderColor = null;
          let boxShadow = null;
        } else if (this.disabled) {
          let boxShadow = null;
          borderColor = '#ebebeb';
        } else if (this.isFocused) {
          // borderColor = 'rgba(var(--vs-primary), 1)';
          // boxShadow = '0 3px 10px 0 rgba(0,0,0,.15)';
        } else {
          let boxShadow = null;
          borderColor = 'lightgray';
        }
        style['border'] = borderColor ? `1px solid ${ borderColor }` : '';
        style['boxShadow'] = boxShadow;
        return style;
      },
      getSearchContainerClass: function () {
        let marginClass = this.size === 'smaller' ? 'mt--5' : '';
        if (this.disabled) {
          return marginClass + ' ' + ('multi-select-text-disabled');
        }
        return marginClass + ' ' + (this.selectedItemsText ? 'multi-select-text-dark' : 'multi-select-text-light');
      },
      iconDecider: function () {
        if (! this.isFocused) {
          return `${ this.icon } ${ this.iconPack }`;
        } else if (this.isFocused && this.mode === 'default') {
          return `${ this.icon } ${ this.iconPack } 'fa-rotate-180'`;
        } else if (this.isFocused && this.mode === 'report-filter') {
          return `${ this.iconSearch }`;
        } else {
          return '';
        }
      },
      optionsDisplayStyle: function () {
        if (this.allowAllSelection) {
          return {
            'max-height': '240px',
            'padding-bottom': (this.dropdown === 'top' ? '15px' : '0')
          };
        } else {
          return {
            'max-height': '280px',
            'padding-bottom': (this.dropdown === 'top' ? '15px' : '5px')
          };
        }
      },
    },
    watch: {
      disabled: function () {
        this.closeSelect();
      },
      value: function () {
        this.updateSelectedText();
      },
      searchKeyword: function () {
        this.setOptionsStyle();
        this.$refs['multi-select-input'].focus();
      },
    },
    mounted: function () {
      this.$forceUpdate();
      this.isMounted = true;
      this.updateSelectedText();
      this.setOptionsStyle();
      this.setScrollListeners();
    },
    beforeDestroy () {
      this.destroyParentScrollListeners();
      this.destroyIntersectionObserver();
      this.closeSelect();
    },
    methods: {
      setScrollListeners: function () {
        let node = this.$refs['select-parent-container'];
        if (node) {
          this.setParentScrollListeners(node, this.setOptionsStyle);
        }
        let inputField = this.$refs['multi-select-selected-text'];
        if (inputField) {
          //CLOSING SELECT WHEN MULTISELECT GETS OUT OF SIGHT WHEN SCROLLING.
          this.setIntersectionObserver(inputField, this.closeSelect);
        }
      },
      setOptionsStyle: function () {
        if (! this.showOptions) return;
        let vertical = 'top';
        let totalAvailableHeight = window.innerHeight;
        let position;
        const parentContainerRect = this.$refs['select-parent-container'].getBoundingClientRect();
        let options = [];
        for (let i = 0; i < this.$children.length; i++) {
          if (this.$children[i]['isShow']) {
            options.push(this.$children[i]);
          }
        }
        const optionCount = options.length;
        // 34.43 : height of option 29.43 + 5px margin
        // 25 : bottom padding of option container 15px + 10px top padding
        let optionContainerHeight =
          Math.min(((optionCount * 34.43) + 25 + (this.allowAllSelection ? 34.43 : 0)), 280);

        position = parentContainerRect.bottom;
        if ((position + optionContainerHeight) > totalAvailableHeight) {
          this.dropdown = 'top';
          position = parentContainerRect.top - optionContainerHeight;
        } else {
          this.dropdown = 'bottom';
        }
        let width =
          (this.maxContentWidth ? 'max-content'
            : (this.autoComplete ? (this.optionContainerWidth + 2 + 'px') : (this.optionContainerWidth + 2 + 'px')));
        let left = (parentContainerRect.left - (this.autoComplete ? 0 : 0)) + 'px';
        let style = {
          'width': width,
          'left': left,
          'position': 'fixed',
          'border-bottom': '1px solid lightgray',
          'border-left': '1px solid lightgray',
          'border-right': '1px solid lightgray',
          'box-shadow':
            (this.mode === 'default' || this.mode === 'conditional-formatting')
              ? '0 3px 8px 0 rgba(0, 0, 0, 0.2)'
              : '',
          'overflow-y': 'hidden',
          'max-height': '280px',
          'background': this.mode === 'report-filter' ? 'white' : '#FFFFFF',
          'border-radius': (
            this.mode === 'report-filter'
              ? (this.dropdown === 'bottom' ? '0 0 20px 20px' : '20px 20px 0 0')
              : (this.mode === 'conditional-formatting'
                  ? '5px'
                  : (this.dropdown === 'bottom' ? '0 0 4px 4px' : '4px 4px 0 0')
              )
          ),
        };

        let invertedCornerPosition = (optionContainerHeight - 6) + 'px';
        this.dropdownInvertedCornerStyle = {
          'top': invertedCornerPosition,
        };

        style[vertical] = position + 'px';
        this.optionsContainerStyle = style;
        document.body.prepend(this.$refs['options-container']);
      },
      updateSelectedText: function () {
        let currentTexts = [];
        let selectItems = this.$children;
        if (this.allowAllSelection) {
          // selectItems.splice(0, 1);
        }
        if (this.value && selectItems) {
          this.isSelectAllSelected = this.$children
            .filter(child => child.$options['_componentTag'] === 'multi-select-item')
            .every(multiSelectItem => multiSelectItem['selected']);
        } else {
          this.isSelectAllSelected = false;
        }
        if (Array.isArray(this.value)) {
          this.value.forEach(value => {
            let valuePresentInChild = false;
            for (let index = 0; index < selectItems.length; index++) {
              let selectItem = selectItems[index];
              if (value === selectItem['value']) {
                currentTexts.push(selectItem['text']);
                valuePresentInChild = true;
                break;
              }
            }
            if (! valuePresentInChild && this.customValueEnabled) {
              currentTexts.push(value);
            }
          });
        } else {
          let valuePresentInChild = false;
          for (let index = 0; index < selectItems.length; index++) {
            let selectItem = selectItems[index];
            if (this.value === selectItem['value']) {
              currentTexts.push(selectItem['text']);
              valuePresentInChild = true;
              break;
            }
          }
          if (! valuePresentInChild && this.customValueEnabled) {
            currentTexts.push(this.value);
          }
        }
        this.selectedItems = currentTexts;
        this.selectedItemsText = currentTexts.join(',');
      },
      handleKeyPress: function (event) {
        let key = event['key'];
        let eventHandlers = {
          'ArrowDown': this.handleKeyDown,
          'ArrowUp': this.handleKeyUp,
          'Home': this.handleHome,
          'End': this.handleEnd,
          'Enter': this.handleSearchEnter,
        };
        if (eventHandlers[key]) {
          eventHandlers[key](event
          );
        }
      },
      getChildren: function () {
        return this.getAllChildrenByName(this, 'MultiSelectItem').filter(a => a['isShow']);
      },
      setActiveMultiSelectItemIndex: function (children, index) {
        if (! this.allowKeyNavigation) return;
        try {
          this.activeMultiSelectItemIndex = index;
          this.$refs['multiselectItemContainer'].scrollTop = this.$refs['multiselectItemContainer'].scrollTop +
            children[this.activeMultiSelectItemIndex].$el.getBoundingClientRect()['y'] - 280;
        } catch (e) {
        }
      },
      handleHome: function () {
        if (! this.allowKeyNavigation) return;
        this.setActiveMultiSelectItemIndex(this.getChildren(), 0);
      },
      handleEnd: function () {
        if (! this.allowKeyNavigation) return;
        let children = this.getChildren();
        this.setActiveMultiSelectItemIndex(children, children.length - 1);
      },
      handleKeyDown: function () {
        if (! this.allowKeyNavigation) return;
        let children = this.getChildren();
        let childrenCount = children.length;
        if (childrenCount < 1) return;
        this.setActiveMultiSelectItemIndex(children, (this.activeMultiSelectItemIndex + 1) % childrenCount);
      },
      handleKeyUp: function () {
        if (! this.allowKeyNavigation) return;
        let children = this.getChildren();
        let childrenCount = children.length;
        if (childrenCount < 1) return;
        this.setActiveMultiSelectItemIndex(children,
          (this.activeMultiSelectItemIndex + (childrenCount - 1)) % childrenCount);
      },
      handleSearchEnter: function () {
        if (! this.allowKeyNavigation) return;
        if (! this.showOptions) return;
        if (this.activeMultiSelectItemIndex !== -1) {
          try {
            let searchKeyword = this.searchKeyword;
            let activeMultiSelectItemIndex = this.activeMultiSelectItemIndex;
            this.getChildren()[this.activeMultiSelectItemIndex].selectOption();
            this.openSelect();
            this.searchKeyword = searchKeyword;
            this.setActiveMultiSelectItemIndex(this.getChildren(), activeMultiSelectItemIndex);
          } catch (e) {
          }
        }
      },
      handleEscape: function () {
        if (this.searchKeyword.length > 0) this.searchKeyword = '';
        else if (this.searchKeyword.length === 0) {
          this.closeSelect();
          if (this.autoComplete)
            this.$refs['multi-select-input'].blur();
        }
      },
      handleEnter: function () {
        let value = this.$refs['multi-select-input'].value;
        if (this.customValueEnabled && value.length > 0) {
          let valuePresent = false;
          if (this.multiple) {
            (Array.isArray(this.value) ? this.value : [this.value]).forEach(selectedValue => {
              if (selectedValue === value) {
                valuePresent = true;
              }
            });
          } else {
            if (Array.isArray(this.value)) {
              if (this.value[0] === value) {
                valuePresent = true;
              }
            } else {
              if (this.value === value) {
                valuePresent = true;
              }
            }
          }
          let action = (valuePresent ? 'remove' : 'add');
          this.selectOption(value, value, action);
          this.$refs['multi-select-input'].value = '';
        }
      },
      openSelect: function () {
        if (! this.showOptions && ! this.disabled) {
          this.$nextTick(() => {
            this.setOptionsStyle();
          });
          if (this.autoComplete) {
            setTimeout(() => {
              this.$refs['multi-select-input'].focus();
            }, 200);
          }
          this.changeView(true);
          this.isFocused = true;
        }
        this.activeMultiSelectItemIndex = -1;
      },
      closeSelect: function () {
        if (this.showOptions) {
          this.searchKeyword = '';
          this.changeView(false);
          if (this.autoComplete) {
            this.$refs['multi-select-input'].blur();
          }
          document.body.removeChild(this.$refs['options-container']);
          this.$emit('close');
        }
        this.isFocused = false;
      },
      toggleSelect: function (force = false) {
        if (this.showOptions && (force || this.closeOnToggle))
          this.closeSelect();
        else {
          this.openSelect();
          this.$emit('open');
        }
      },
      changeView: function (state) {
        this.showOptions = state;
      },
      selectAllOptions: function () {
        this.isSelectAllSelected = ! this.isSelectAllSelected;
        let values = [];
        if (this.isSelectAllSelected) {
          if (this.multiple) {
            for (let i = 0; i < this.$children.length; i++) {
              if (this.$children[i].$options['_componentTag'] === 'multi-select-item') {
                if (this.maximum !== -1 && values.length >= this.maximum) {
                  break;
                }
                values.push(this.$children[i]['value']);
              }
            }
            this.$emit('input', values);
            this.$emit('change', values);
          }
        } else {
          this.$emit('input', values);
          this.$emit('change', values);
        }
      },
      selectOption: function (optionValue, optionText, action) {
        let valueChanged = false;
        let values = [];
        if (Array.isArray(this.value)) {
          values = [...this.value];
        } else {
          if (this.value) {
            if (typeof this.value === 'string') {
              if (this.value.length > 0) {
                values.push(this.value);
              }
            } else {
              values.push(this.value);
            }
          }
        }

        if (action === 'remove') {
          if (values.length > this.minimum) {
            let optionIndex = values.indexOf(optionValue);
            if (optionIndex !== -1) {
              values.splice(optionIndex, 1);
              valueChanged = true;
            }
          }
        } else if (action === 'add') {
          if (this.multiple) {
            if (this.maximum === -1 || values.length < this.maximum) {
              values.push(optionValue);
              valueChanged = true;
            } else if (this.overrideSelectedValues && values.length === this.maximum && this.maximum > 0) {
              if (this.overridePosition === 'start') {
                values.shift();
                values.push(optionValue);
              } else if (this.overridePosition === 'end') {
                values[this.maximum - 1] = optionValue;
              }
              valueChanged = true;
            }
          } else {
            values = [];
            values.push(optionValue);
            valueChanged = true;
          }
        }

        //EMITTING INPUT EVENT
        if (valueChanged) {
          let emittingValue;
          if (this.multiple) {
            emittingValue = values;
            if (values.length === this.maximum) {
              this.closeSelect();
              this.handleEscape();
            }
            if (values.length === 0 && this.emitNullOnEmpty) {
              emittingValue = null;
            }
          } else {
            this.closeSelect();
            this.handleEscape();
            if (values.length < 0) {
              emittingValue = null;
            } else {
              emittingValue = values[0];
            }
          }
          this.$emit('input', emittingValue);
          this.$emit('change', optionValue);
        }
      },
      removeSelectedItem: function (text, index) {
        let action = 'remove';
        let value = this.value[index];
        this.selectOption(value, text, action);
      },
      appendOptions: function () {
        this.$emit('append-options');
      },
    }
  };
</script>

<style lang="scss" scoped>
  input:focus {
    outline-offset: -2px;
  }

  .multiselect-container {
    position: relative;

    &.multiselect-small {
      .input-container {
        min-height: 35px;
      }
    }

    &.multiselect-regular {
      .input-container {
        min-height: 40px;
      }

      .label-text {
        font-size: 16px;
      }
    }

    &.multiselect-large {
      .input-container {
        min-height: 50px;
      }

      .label-text {
        font-size: 18.4px;
      }
    }

    .input-container {
      border-radius: 4px;
      display: flex;
      flex-wrap: wrap;
      align-content: center;
      justify-items: center;
      justify-content: center;
      border: none;

      &.input-container-report-filter {
        background: white;
        border-radius: 1.5rem;
      }

      &:focus {
        cursor: text;
      }
    }

    .search-container {
      width: 90%;

      &.no-icon {
        width: 100%;
      }

      &.search-container-report-filter {
        width: 85%;
      }

      .search-input {
        background-color: inherit;
        cursor: pointer;

        &:focus {
          cursor: text;
        }
      }
    }

    .icons-container {
      width: 10%;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      color: rgba(0, 0, 0, 0.4);

      &.icons-container-report-filter {
        justify-content: center;
        width: 15%;

      }

      .icon-down-container {
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        height: 25px;
        width: 25px;
      }
    }


    .options-container {
      width: 100%;
      position: fixed;
      border-radius: 5px;
      overflow-y: hidden;

      &:hover {
        overflow-y: auto;
      }

      .multi-select-input {
        color: gray;
        box-shadow: none !important;
      }
    }
  }

  .multi-select-text-disabled {
    &::placeholder {
      color: rgba(#626262, 0.75);
    }
  }

  .multi-select-text-light {
    &::placeholder {
      color: #999999;
      font-size: 17px !important;
      font-weight: normal;
      opacity: 1;
    }
  }

  .multi-select-text-dark {
    &::placeholder {
      color: #626262;
      font-size: 17px !important;
      font-weight: normal;
      opacity: 1;
    }
  }

  .inverted-corners {
    width: 100%;
    height: 10px;
    background-color: #FFFFFF;

    &.dropdown-bottom {
      border-bottom-left-radius: 100px;
      border-bottom-right-radius: 100px;
      border: 1px solid lightgray;
      margin-top: -3px;
    }

    &.dropdown-top {
      border-top-left-radius: 100px;
      border-top-right-radius: 100px;
      position: relative;
    }
  }

  .select-all {
    padding: 5px 15px;

    .select-all-selected {
      width: 13px;
      height: 13px;
      border-radius: 50%;
      border: 1px solid grey;
      margin-right: 10px;

      &.filled {
        background-color: rgba(var(--vs-primary), 1);
      }
    }
  }

  .tags-display {
    width: 117% !important;
    height: inherit;
  }
</style>