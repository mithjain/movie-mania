export const domMixins = {
  data: function () {
    return {
      clientXMultiplier: 1.25,
      clientYMultiplier: 1.25
    };
  },
  methods: {
    scrollToElement: function (parent, child, offsetTop = 0) {
      let parentRect = parent.getBoundingClientRect();
      if (! (parent && child)) return;
      let parentViewableArea = {
        height: parent.clientHeight,
        width: parent.clientWidth
      };
      let childRect = child.getBoundingClientRect();
      let isViewable =
        (childRect.top >= parentRect.top)
        && (childRect.top <= parentRect.top + parentViewableArea.height);
      if (! isViewable) {
        parent.scrollTop = (childRect.top + parent.scrollTop) - (parentRect.top + offsetTop);
      }
    },
    getEventProperty: function (event, property, multiplier = undefined) {
      let propertyToMultiplierMap = {
        'clientX': this.clientXMultiplier,
        'clientY': this.clientYMultiplier,
        'screenX': this.clientXMultiplier,
        'screenY': this.clientYMultiplier,
        'layerX': this.clientXMultiplier,
        'layerY': this.clientYMultiplier,
      };
      return event[property] * (multiplier || propertyToMultiplierMap[property] || 1);
    },
    getCursorPosition: function (event, x_offset = 0, y_offset = 0, multiplier = undefined) {
      let cursorEvent = event || window.event;
      let left = this.getEventProperty(cursorEvent, 'clientX', multiplier) + x_offset,
        top = this.getEventProperty(cursorEvent, 'clientY', multiplier) + y_offset;
      return { 'x': left, 'y': top };
    },
  }
};