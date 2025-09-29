// Desktop Footer Component
// Multi-column layout with detailed information and refined spacing

class DesktopFooter {
  constructor(options = {}) {
    this.options = {
      containerId: 'desktop-footer',
      companyName: 'Ascend Institute',
      year: new Date().getFullYear(),
      showSocial: true,
      showNewsletter: true,
      columns: 4,
      ...options
    };
    
    this.init();
  }

  init() {
    this.render();
    this.attachEventListeners();
  }

  render() {
    const container = document.getElementById(this.options.containerId) || document.body;
    
    const footerHTML = `
      <footer class="footer-desktop" id="desktop-footer-component">
        <div class="footer-container">
          
          <!-- Main Footer Content -->
          <div class="footer-content">
            
            <!-- Company Info Column -->
            <div class="footer-column">
              <div class="footer-brand">
                <h3 class="footer-logo">${this.options.companyName}</h3>
                <p class="footer-tagline">Sovereign Stack Technology</p>
              </div>
              <p class="footer-description">
                Empowering individuals through education, technology, and financial autonomy. 
                Building the future of sovereign digital infrastructure with GremlinGPT, 
                self-hosting solutions, and comprehensive learning resources.
              </p>
              ${this.options.showSocial ? this.renderSocial() : ''}
            </div>

            <!-- Quick Links Column -->
            <div class="footer-column">
              <h4 class="footer-title">Navigation</h4>
              <ul class="footer-links">
                <li><a href="/" class="footer-link">Home</a></li>
                <li><a href="/about" class="footer-link">About Us</a></li>
                <li><a href="/courses" class="footer-link">Courses</a></li>
                <li><a href="/resources" class="footer-link">Resources</a></li>
                <li><a href="/community" class="footer-link">Community</a></li>
                <li><a href="/blog" class="footer-link">Blog</a></li>
                <li><a href="/contact" class="footer-link">Contact</a></li>
              </ul>
            </div>

            <!-- Programs Column -->
            <div class="footer-column">
              <h4 class="footer-title">Programs & Services</h4>
              <ul class="footer-links">
                <li><a href="/gremlingpt" class="footer-link">GremlinGPT AI System</a></li>
                <li><a href="/sovereign-stack" class="footer-link">Sovereign Stack</a></li>
                <li><a href="/financial-autonomy" class="footer-link">Financial Autonomy</a></li>
                <li><a href="/self-hosting" class="footer-link">Self-Hosting Solutions</a></li>
                <li><a href="/consulting" class="footer-link">Technical Consulting</a></li>
                <li><a href="/workshops" class="footer-link">Workshops & Training</a></li>
              </ul>
            </div>

            <!-- Support & Resources Column -->
            <div class="footer-column">
              <h4 class="footer-title">Support & Resources</h4>
              <ul class="footer-links">
                <li><a href="/help" class="footer-link">Help Center</a></li>
                <li><a href="/docs" class="footer-link">Documentation</a></li>
                <li><a href="/api" class="footer-link">API Reference</a></li>
                <li><a href="/faq" class="footer-link">FAQ</a></li>
                <li><a href="/status" class="footer-link">Service Status</a></li>
                <li><a href="/changelog" class="footer-link">Changelog</a></li>
              </ul>
            </div>

          </div>

          ${this.options.showNewsletter ? this.renderNewsletter() : ''}

          <!-- Footer Bottom -->
          <div class="footer-bottom">
            <div class="footer-bottom-left">
              <p class="footer-copyright">
                &copy; ${this.options.year} ${this.options.companyName}. All rights reserved.
              </p>
              <div class="footer-legal">
                <a href="/privacy" class="footer-legal-link">Privacy Policy</a>
                <span class="footer-separator">•</span>
                <a href="/terms" class="footer-legal-link">Terms of Service</a>
                <span class="footer-separator">•</span>
                <a href="/cookies" class="footer-legal-link">Cookie Policy</a>
              </div>
            </div>
            <div class="footer-bottom-right">
              <p class="footer-built-with">
                Built with ❤️ for digital sovereignty
                <span class="footer-tech-stack">• React • Node.js • AI</span>
              </p>
            </div>
          </div>

        </div>
      </footer>
      
      <style>
        .footer-desktop {
          background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
          color: #e2e8f0;
          margin-top: 4rem;
        }
        
        .footer-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 2rem;
        }
        
        .footer-content {
          display: grid;
          grid-template-columns: 2fr 1fr 1fr 1fr;
          gap: 3rem;
          padding: 3rem 0 2rem;
          border-bottom: 1px solid #334155;
        }
        
        .footer-column {
          display: flex;
          flex-direction: column;
        }
        
        .footer-brand {
          margin-bottom: 1.5rem;
        }
        
        .footer-logo {
          font-size: 1.5rem;
          font-weight: bold;
          color: #f8fafc;
          margin: 0 0 0.25rem 0;
        }
        
        .footer-tagline {
          font-size: 0.875rem;
          color: #94a3b8;
          margin: 0;
          font-style: italic;
        }
        
        .footer-description {
          font-size: 0.875rem;
          line-height: 1.6;
          color: #cbd5e1;
          margin: 0 0 2rem 0;
          max-width: 90%;
        }
        
        .footer-title {
          font-size: 1rem;
          font-weight: 600;
          color: #f8fafc;
          margin: 0 0 1.5rem 0;
        }
        
        .footer-links {
          list-style: none;
          padding: 0;
          margin: 0;
        }
        
        .footer-links li {
          margin-bottom: 0.75rem;
        }
        
        .footer-link {
          color: #cbd5e1;
          text-decoration: none;
          font-size: 0.875rem;
          line-height: 1.5;
          transition: all 0.2s ease;
          display: inline-block;
        }
        
        .footer-link:hover {
          color: #f8fafc;
          transform: translateX(4px);
        }
        
        /* Newsletter Section */
        .newsletter-section {
          background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
          padding: 2.5rem;
          margin: 2rem 0;
          border-radius: 12px;
          border: 1px solid #475569;
        }
        
        .newsletter-content {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 3rem;
          align-items: center;
        }
        
        .newsletter-info h4 {
          font-size: 1.25rem;
          font-weight: 600;
          color: #f8fafc;
          margin: 0 0 0.5rem 0;
        }
        
        .newsletter-info p {
          font-size: 0.9rem;
          color: #cbd5e1;
          margin: 0;
          line-height: 1.6;
        }
        
        .newsletter-form {
          display: flex;
          gap: 1rem;
          max-width: 400px;
        }
        
        .newsletter-input {
          flex: 1;
          padding: 0.75rem 1rem;
          border: 1px solid #475569;
          border-radius: 8px;
          background: #334155;
          color: #f8fafc;
          font-size: 0.9rem;
          transition: all 0.2s ease;
        }
        
        .newsletter-input:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
          background: #1e293b;
        }
        
        .newsletter-input::placeholder {
          color: #94a3b8;
        }
        
        .newsletter-button {
          background: #3b82f6;
          color: white;
          border: none;
          padding: 0.75rem 1.5rem;
          border-radius: 8px;
          font-weight: 500;
          font-size: 0.9rem;
          cursor: pointer;
          transition: all 0.2s ease;
          white-space: nowrap;
        }
        
        .newsletter-button:hover {
          background: #2563eb;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        .newsletter-button:active {
          transform: translateY(0);
        }
        
        /* Social Links */
        .social-links {
          display: flex;
          gap: 1rem;
          margin-top: 1rem;
        }
        
        .social-link {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          background: #334155;
          color: #cbd5e1;
          text-decoration: none;
          border-radius: 8px;
          transition: all 0.2s ease;
        }
        
        .social-link:hover {
          background: #3b82f6;
          color: white;
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        /* Footer Bottom */
        .footer-bottom {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 2rem 0;
          border-top: 1px solid #334155;
          margin-top: 2rem;
        }
        
        .footer-bottom-left {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .footer-copyright {
          font-size: 0.875rem;
          color: #94a3b8;
          margin: 0;
        }
        
        .footer-legal {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        
        .footer-legal-link {
          font-size: 0.8rem;
          color: #64748b;
          text-decoration: none;
          transition: color 0.2s ease;
        }
        
        .footer-legal-link:hover {
          color: #cbd5e1;
        }
        
        .footer-separator {
          color: #475569;
          font-size: 0.8rem;
        }
        
        .footer-bottom-right {
          text-align: right;
        }
        
        .footer-built-with {
          font-size: 0.8rem;
          color: #64748b;
          margin: 0;
        }
        
        .footer-tech-stack {
          display: block;
          font-size: 0.75rem;
          color: #475569;
          margin-top: 0.25rem;
        }
        
        /* Hide on mobile */
        @media (max-width: 768px) {
          .footer-desktop {
            display: none;
          }
        }
        
        /* Tablet adjustments */
        @media (max-width: 1024px) {
          .footer-content {
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
          }
          
          .footer-column:first-child {
            grid-column: 1 / -1;
            margin-bottom: 1rem;
          }
          
          .newsletter-content {
            grid-template-columns: 1fr;
            gap: 2rem;
            text-align: center;
          }
          
          .newsletter-form {
            max-width: none;
          }
        }
        
        /* Large desktop optimizations */
        @media (min-width: 1400px) {
          .footer-container {
            max-width: 1400px;
          }
          
          .footer-content {
            gap: 4rem;
            padding: 4rem 0 3rem;
          }
        }
      </style>
    `;
    
    if (container.id === this.options.containerId) {
      container.innerHTML = footerHTML;
    } else {
      container.insertAdjacentHTML('beforeend', footerHTML);
    }
  }

  renderNewsletter() {
    return `
      <div class="newsletter-section">
        <div class="newsletter-content">
          <div class="newsletter-info">
            <h4>Stay Connected</h4>
            <p>
              Get the latest updates on GremlinGPT developments, new courses, 
              technical insights, and community events. Join our growing network 
              of digital sovereignty advocates.
            </p>
          </div>
          <form class="newsletter-form" id="newsletter-form">
            <input 
              type="email" 
              class="newsletter-input" 
              placeholder="Enter your email address"
              required
              id="newsletter-email"
            />
            <button type="submit" class="newsletter-button">
              Subscribe
            </button>
          </form>
        </div>
      </div>
    `;
  }

  renderSocial() {
    return `
      <div class="social-links">
        <a href="https://github.com/statikfintechllc" class="social-link" aria-label="GitHub">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
          </svg>
        </a>
        <a href="https://twitter.com/statikfintech" class="social-link" aria-label="Twitter">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
          </svg>
        </a>
        <a href="https://linkedin.com/company/statikfintech" class="social-link" aria-label="LinkedIn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
          </svg>
        </a>
        <a href="https://discord.gg/ascendinstitute" class="social-link" aria-label="Discord">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419-.0002 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1568 2.4189Z"/>
          </svg>
        </a>
        <a href="mailto:contact@ascendinstitute.tech" class="social-link" aria-label="Email">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
          </svg>
        </a>
      </div>
    `;
  }

  attachEventListeners() {
    // Newsletter form submission
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
      newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.handleNewsletterSubmission();
      });
    }
    
    // Handle responsive behavior
    window.addEventListener('resize', () => {
      if (window.innerWidth <= 768) {
        this.destroy();
      }
    });
  }

  handleNewsletterSubmission() {
    const emailInput = document.getElementById('newsletter-email');
    const button = document.querySelector('.newsletter-button');
    
    if (emailInput && button) {
      const email = emailInput.value.trim();
      
      if (email) {
        // Disable button during submission
        const originalText = button.textContent;
        button.textContent = 'Subscribing...';
        button.disabled = true;
        
        // Simulate API call (replace with actual implementation)
        setTimeout(() => {
          button.textContent = 'Subscribed!';
          button.style.background = '#22c55e';
          emailInput.value = '';
          
          // Reset button after 3 seconds
          setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '#3b82f6';
            button.disabled = false;
          }, 3000);
        }, 1000);
        
        // Fire custom event
        const event = new CustomEvent('newsletterSubscribe', {
          detail: { email, platform: 'desktop' }
        });
        document.dispatchEvent(event);
      }
    }
  }

  updateCompanyInfo(name, year) {
    this.options.companyName = name;
    this.options.year = year;
    
    const logo = document.querySelector('.footer-logo');
    const copyright = document.querySelector('.footer-copyright');
    
    if (logo) logo.textContent = name;
    if (copyright) copyright.textContent = `© ${year} ${name}. All rights reserved.`;
  }

  addFooterLink(columnTitle, text, href) {
    const titles = document.querySelectorAll('.footer-title');
    const targetColumn = Array.from(titles).find(t => t.textContent === columnTitle)?.parentElement;
    
    if (targetColumn) {
      const linksList = targetColumn.querySelector('.footer-links');
      if (linksList) {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = href;
        a.className = 'footer-link';
        a.textContent = text;
        li.appendChild(a);
        linksList.appendChild(li);
      }
    }
  }

  setNewsletterText(title, description) {
    const titleEl = document.querySelector('.newsletter-info h4');
    const descEl = document.querySelector('.newsletter-info p');
    
    if (titleEl) titleEl.textContent = title;
    if (descEl) descEl.textContent = description;
  }

  destroy() {
    const footer = document.getElementById('desktop-footer-component');
    if (footer) {
      footer.remove();
    }
  }
}

// Auto-initialize on DOM ready
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    if (window.innerWidth > 768) {
      new DesktopFooter();
    }
  });
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = DesktopFooter;
}