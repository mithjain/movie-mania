export const scrollerMixin = {
  'name': 'scrollerMixin',
  data: function () {
    return {
      scrollableParents: [],
      scrollHandler: null,
      intersectionObserverNode: null,
      intersectionObserver: null,
    };
  },
  methods: {
    /**
     *
     * @param node
     * @param handler
     * sets a scroll event handler for all the ancestor nodes of the given node and executes handler on scroll.
     */
    setParentScrollListeners: function (node, handler) {
      this.scrollHandler = handler;
      while (node.nodeName !== 'BODY') {
        let properties = window.getComputedStyle(node, null);
        let overflow = properties.getPropertyValue('overflow');
        let overflowY = properties.getPropertyValue('overflow-y');
        if (overflow === 'auto' || overflowY === 'auto') {
          node.addEventListener('scroll', this.scrollHandler, { passive: true });
          this.scrollableParents.push(node);
        }
        node = node.parentNode;
      }
    },
    /**
     * removes all event listeners for all ancestor nodes of passed node.
     */
    destroyParentScrollListeners: function () {
      this.scrollableParents.forEach(node => {
        node.removeEventListener('scroll', this.scrollHandler);
      });
    },
    /**
     *
     * @param node
     * @param handler
     * Starts observing the position change of intersectionObserverNode.
     */
    setIntersectionObserver: function (node, handler) {
      this.intersectionObserverNode = node;
      this.intersectionObserver = new IntersectionObserver((entries) => {
        if (! (entries[0].isIntersecting)) {
          handler();
        }
      }, { threshold: [0] });
      this.intersectionObserver.observe(node);
    },
    /**
     * Stops observing the position change of intersectionObserverNode
     */
    destroyIntersectionObserver: function () {
      if (this.intersectionObserver) {
        this.intersectionObserver.unobserve(this.intersectionObserverNode);
      }
    },
  }
};