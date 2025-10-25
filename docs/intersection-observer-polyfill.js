/**
 * IntersectionObserver polyfill for older browsers
 * Lightweight fallback that provides basic functionality
 */
(function(window, document) {
  'use strict';

  // Exit early if IntersectionObserver is already supported
  if ('IntersectionObserver' in window &&
      'IntersectionObserverEntry' in window &&
      'intersectionRatio' in window.IntersectionObserverEntry.prototype) {
    return;
  }

  /**
   * Simple polyfill using scroll and resize events
   * This is a minimal implementation for fallback support
   */
  function IntersectionObserver(callback, options) {
    this.callback = callback;
    this.options = options || {};
    this.root = this.options.root || null;
    this.rootMargin = this.options.rootMargin || '0px';
    this.thresholds = this.options.threshold || [0];
    this.observedElements = [];

    if (!Array.isArray(this.thresholds)) {
      this.thresholds = [this.thresholds];
    }

    // Throttle check to improve performance
    this._checkIntersections = this._throttle(function() {
      var entries = [];
      this.observedElements.forEach(function(element) {
        if (element && element.target) {
          var entry = this._getIntersectionEntry(element.target);
          entries.push(entry);
        }
      }.bind(this));

      if (entries.length > 0) {
        this.callback(entries, this);
      }
    }.bind(this), 100);

    // Set up event listeners for scroll and resize
    this._setupListeners();
  }

  IntersectionObserver.prototype._setupListeners = function() {
    if (typeof window !== 'undefined') {
      window.addEventListener('scroll', this._checkIntersections, true);
      window.addEventListener('resize', this._checkIntersections, true);
    }
  };

  IntersectionObserver.prototype._removeListeners = function() {
    if (typeof window !== 'undefined') {
      window.removeEventListener('scroll', this._checkIntersections, true);
      window.removeEventListener('resize', this._checkIntersections, true);
    }
  };

  IntersectionObserver.prototype._throttle = function(func, wait) {
    var timeout = null;
    var previous = 0;
    
    return function() {
      var now = Date.now();
      var remaining = wait - (now - previous);
      var context = this;
      var args = arguments;
      
      if (remaining <= 0 || remaining > wait) {
        if (timeout) {
          clearTimeout(timeout);
          timeout = null;
        }
        previous = now;
        func.apply(context, args);
      } else if (!timeout) {
        timeout = setTimeout(function() {
          previous = Date.now();
          timeout = null;
          func.apply(context, args);
        }, remaining);
      }
    };
  };

  IntersectionObserver.prototype._getIntersectionEntry = function(element) {
    var rect = element.getBoundingClientRect();
    var rootRect = this.root ? this.root.getBoundingClientRect() : {
      top: 0,
      left: 0,
      bottom: window.innerHeight,
      right: window.innerWidth,
      width: window.innerWidth,
      height: window.innerHeight
    };

    var intersectionRect = {
      top: Math.max(rect.top, rootRect.top),
      left: Math.max(rect.left, rootRect.left),
      bottom: Math.min(rect.bottom, rootRect.bottom),
      right: Math.min(rect.right, rootRect.right)
    };

    intersectionRect.width = Math.max(0, intersectionRect.right - intersectionRect.left);
    intersectionRect.height = Math.max(0, intersectionRect.bottom - intersectionRect.top);

    var intersectionArea = intersectionRect.width * intersectionRect.height;
    var elementArea = rect.width * rect.height;
    var intersectionRatio = elementArea > 0 ? intersectionArea / elementArea : 0;

    var isIntersecting = intersectionRatio > 0;

    return {
      target: element,
      boundingClientRect: rect,
      rootBounds: rootRect,
      intersectionRect: intersectionRect,
      intersectionRatio: intersectionRatio,
      isIntersecting: isIntersecting,
      time: Date.now()
    };
  };

  IntersectionObserver.prototype.observe = function(element) {
    if (!element) return;
    
    // Avoid duplicate observations
    var alreadyObserved = this.observedElements.some(function(item) {
      return item.target === element;
    });

    if (!alreadyObserved) {
      this.observedElements.push({ target: element });
      // Trigger initial check
      requestAnimationFrame(this._checkIntersections);
    }
  };

  IntersectionObserver.prototype.unobserve = function(element) {
    this.observedElements = this.observedElements.filter(function(item) {
      return item.target !== element;
    });
  };

  IntersectionObserver.prototype.disconnect = function() {
    this.observedElements = [];
    this._removeListeners();
  };

  IntersectionObserver.prototype.takeRecords = function() {
    return [];
  };

  // Polyfill window.IntersectionObserver
  window.IntersectionObserver = IntersectionObserver;

  // Stub for IntersectionObserverEntry
  window.IntersectionObserverEntry = function() {};

})(window, document);
