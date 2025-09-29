// Mobile Card Component
// Touch-optimized card component with mobile-friendly interactions

class MobileCard {
  constructor(options = {}) {
    this.options = {
      containerId: null,
      title: 'Card Title',
      description: 'Card description goes here',
      imageUrl: null,
      linkUrl: null,
      linkText: 'Learn More',
      variant: 'default', // default, featured, compact
      showButton: true,
      interactive: true,
      ...options
    };
    
    this.init();
  }

  init() {
    this.render();
    if (this.options.interactive) {
      this.attachEventListeners();
    }
  }

  render() {
    const container = this.options.containerId ? 
      document.getElementById(this.options.containerId) : 
      document.createElement('div');
    
    const cardHTML = `
      <div class="card-mobile ${this.options.variant}" data-card-id="${this.generateId()}">
        ${this.options.imageUrl ? this.renderImage() : ''}
        <div class="card-content">
          <h3 class="card-title">${this.options.title}</h3>
          <p class="card-description">${this.options.description}</p>
          ${this.options.showButton ? this.renderButton() : ''}
        </div>
      </div>
      
      <style>
        .card-mobile {
          background: white;
          border-radius: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          overflow: hidden;
          margin-bottom: 1.5rem;
          transition: all 0.3s ease;
          position: relative;
        }
        
        .card-mobile.interactive {
          cursor: pointer;
        }
        
        .card-mobile.interactive:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }
        
        .card-mobile.interactive:active {
          transform: translateY(0);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Variant styles */
        .card-mobile.featured {
          border: 2px solid #3b82f6;
          box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
        }
        
        .card-mobile.compact {
          margin-bottom: 1rem;
        }
        
        .card-mobile.compact .card-content {
          padding: 1rem;
        }
        
        .card-mobile.compact .card-title {
          font-size: 1rem;
          margin-bottom: 0.5rem;
        }
        
        .card-mobile.compact .card-description {
          font-size: 0.875rem;
          margin-bottom: 0.75rem;
        }
        
        /* Image styles */
        .card-image {
          width: 100%;
          height: 200px;
          object-fit: cover;
          display: block;
        }
        
        .card-image-placeholder {
          width: 100%;
          height: 200px;
          background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          color: #64748b;
          font-size: 0.875rem;
        }
        
        /* Content styles */
        .card-content {
          padding: 1.5rem;
        }
        
        .card-title {
          font-size: 1.125rem;
          font-weight: 600;
          color: #1e293b;
          margin: 0 0 0.75rem 0;
          line-height: 1.4;
        }
        
        .card-description {
          font-size: 0.9rem;
          color: #64748b;
          line-height: 1.6;
          margin: 0 0 1.25rem 0;
        }
        
        /* Button styles */
        .card-button {
          background: #3b82f6;
          color: white;
          border: none;
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          font-size: 0.9rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
          width: 100%;
          min-height: 44px;
          display: flex;
          align-items: center;
          justify-content: center;
          text-decoration: none;
        }
        
        .card-button:hover {
          background: #2563eb;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .card-button:active {
          transform: translateY(0);
          background: #1d4ed8;
        }
        
        .card-button.secondary {
          background: transparent;
          color: #3b82f6;
          border: 2px solid #3b82f6;
        }
        
        .card-button.secondary:hover {
          background: #3b82f6;
          color: white;
        }
        
        /* Loading state */
        .card-mobile.loading {
          pointer-events: none;
          opacity: 0.7;
        }
        
        .card-mobile.loading .card-content::after {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          width: 20px;
          height: 20px;
          border: 2px solid #e2e8f0;
          border-top-color: #3b82f6;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          transform: translate(-50%, -50%);
        }
        
        @keyframes spin {
          to { transform: translate(-50%, -50%) rotate(360deg); }
        }
        
        /* Touch feedback */
        .card-mobile:active {
          background: #f8fafc;
        }
        
        /* Accessibility */
        .card-mobile:focus-within {
          outline: 2px solid #3b82f6;
          outline-offset: 2px;
        }
        
        /* Hide on desktop */
        @media (min-width: 769px) {
          .card-mobile {
            display: none;
          }
        }
        
        /* Very small screens */
        @media (max-width: 320px) {
          .card-content {
            padding: 1rem;
          }
          
          .card-title {
            font-size: 1rem;
          }
          
          .card-description {
            font-size: 0.85rem;
          }
        }
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
          .card-mobile {
            background: #1e293b;
            color: #e2e8f0;
          }
          
          .card-title {
            color: #f8fafc;
          }
          
          .card-description {
            color: #cbd5e1;
          }
          
          .card-mobile:active {
            background: #334155;
          }
        }
      </style>
    `;
    
    if (this.options.containerId) {
      container.innerHTML = cardHTML;
    } else {
      container.innerHTML = cardHTML;
      return container;
    }
  }

  renderImage() {
    if (this.options.imageUrl) {
      return `
        <img 
          src="${this.options.imageUrl}" 
          alt="${this.options.title}"
          class="card-image"
          loading="lazy"
        />
      `;
    } else {
      return `
        <div class="card-image-placeholder">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
            <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
          </svg>
        </div>
      `;
    }
  }

  renderButton() {
    if (this.options.linkUrl) {
      return `
        <a href="${this.options.linkUrl}" class="card-button">
          ${this.options.linkText}
        </a>
      `;
    } else {
      return `
        <button class="card-button" data-action="click">
          ${this.options.linkText}
        </button>
      `;
    }
  }

  attachEventListeners() {
    const card = document.querySelector(`[data-card-id="${this.generateId()}"]`);
    const button = card?.querySelector('.card-button');
    
    if (card && this.options.interactive) {
      // Card click handling
      card.addEventListener('click', (e) => {
        // Don't trigger card click if button was clicked
        if (!e.target.closest('.card-button')) {
          this.onCardClick(e);
        }
      });
      
      // Touch feedback
      card.addEventListener('touchstart', () => {
        card.classList.add('touching');
      });
      
      card.addEventListener('touchend', () => {
        card.classList.remove('touching');
      });
    }
    
    if (button && !this.options.linkUrl) {
      button.addEventListener('click', (e) => {
        e.stopPropagation();
        this.onButtonClick(e);
      });
    }
    
    // Handle image loading errors
    const image = card?.querySelector('.card-image');
    if (image) {
      image.addEventListener('error', () => {
        image.style.display = 'none';
        const placeholder = document.createElement('div');
        placeholder.className = 'card-image-placeholder';
        placeholder.innerHTML = `
          <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
            <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
          </svg>
        `;
        image.parentElement.insertBefore(placeholder, image);
      });
    }
  }

  onCardClick(event) {
    // Default card click behavior
    if (this.options.linkUrl) {
      window.location.href = this.options.linkUrl;
    } else {
      // Fire custom event
      const customEvent = new CustomEvent('cardClick', {
        detail: { 
          cardId: this.generateId(),
          title: this.options.title,
          options: this.options 
        }
      });
      document.dispatchEvent(customEvent);
    }
  }

  onButtonClick(event) {
    // Default button click behavior
    const customEvent = new CustomEvent('cardButtonClick', {
      detail: { 
        cardId: this.generateId(),
        title: this.options.title,
        options: this.options 
      }
    });
    document.dispatchEvent(customEvent);
  }

  generateId() {
    if (!this._id) {
      this._id = 'card-' + Math.random().toString(36).substr(2, 9);
    }
    return this._id;
  }

  setLoading(isLoading) {
    const card = document.querySelector(`[data-card-id="${this.generateId()}"]`);
    if (card) {
      if (isLoading) {
        card.classList.add('loading');
      } else {
        card.classList.remove('loading');
      }
    }
  }

  updateContent(newOptions) {
    this.options = { ...this.options, ...newOptions };
    
    const card = document.querySelector(`[data-card-id="${this.generateId()}"]`);
    if (card) {
      const title = card.querySelector('.card-title');
      const description = card.querySelector('.card-description');
      const button = card.querySelector('.card-button');
      const image = card.querySelector('.card-image');
      
      if (title && newOptions.title) title.textContent = newOptions.title;
      if (description && newOptions.description) description.textContent = newOptions.description;
      if (button && newOptions.linkText) button.textContent = newOptions.linkText;
      if (image && newOptions.imageUrl) image.src = newOptions.imageUrl;
    }
  }

  setVariant(variant) {
    const card = document.querySelector(`[data-card-id="${this.generateId()}"]`);
    if (card) {
      card.classList.remove('default', 'featured', 'compact');
      card.classList.add(variant);
      this.options.variant = variant;
    }
  }

  destroy() {
    const card = document.querySelector(`[data-card-id="${this.generateId()}"]`);
    if (card) {
      card.remove();
    }
  }

  // Static method to create multiple cards
  static createGrid(cardsData, containerSelector) {
    const container = document.querySelector(containerSelector);
    if (!container) return [];
    
    const cards = [];
    cardsData.forEach((cardData, index) => {
      const cardElement = document.createElement('div');
      cardElement.id = `mobile-card-${index}`;
      container.appendChild(cardElement);
      
      const card = new MobileCard({
        ...cardData,
        containerId: cardElement.id
      });
      cards.push(card);
    });
    
    return cards;
  }
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = MobileCard;
}