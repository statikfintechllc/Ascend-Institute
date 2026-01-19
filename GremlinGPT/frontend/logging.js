// Frontend Logging Utility
// Provides structured logging for frontend components

class FrontendLogger {
    constructor(component, subcomponent = null) {
        this.component = component;
        this.subcomponent = subcomponent;
        this.logLevel = localStorage.getItem('gremlin_log_level') || 'info';
    }

    _formatMessage(level, message, data = null) {
        const timestamp = new Date().toISOString();
        const source = this.subcomponent ? `${this.component}/${this.subcomponent}` : this.component;
        
        const logEntry = {
            timestamp,
            level,
            source,
            message,
            data,
            userAgent: navigator.userAgent,
            url: window.location.href
        };

        return logEntry;
    }

    _shouldLog(level) {
        const levels = { debug: 0, info: 1, warning: 2, error: 3 };
        return levels[level] >= levels[this.logLevel];
    }

    _sendToBackend(logEntry) {
        // Send critical logs to backend for persistence
        if (logEntry.level === 'error' || logEntry.level === 'warning') {
            fetch('/api/frontend-logs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(logEntry)
            }).catch(err => {
                console.error('Failed to send log to backend:', err);
            });
        }
    }

    debug(message, data = null) {
        if (!this._shouldLog('debug')) return;
        
        const logEntry = this._formatMessage('debug', message, data);
        console.debug(`[${logEntry.source}] ${message}`, data || '');
    }

    info(message, data = null) {
        if (!this._shouldLog('info')) return;
        
        const logEntry = this._formatMessage('info', message, data);
        console.info(`[${logEntry.source}] ${message}`, data || '');
    }

    warning(message, data = null) {
        if (!this._shouldLog('warning')) return;
        
        const logEntry = this._formatMessage('warning', message, data);
        console.warn(`[${logEntry.source}] ${message}`, data || '');
        this._sendToBackend(logEntry);
    }

    error(message, data = null) {
        if (!this._shouldLog('error')) return;
        
        const logEntry = this._formatMessage('error', message, data);
        console.error(`[${logEntry.source}] ${message}`, data || '');
        this._sendToBackend(logEntry);
    }

    performance(operation, duration, data = null) {
        const logEntry = this._formatMessage('info', `Performance: ${operation} took ${duration}ms`, data);
        console.log(`[PERF][${logEntry.source}] ${operation}: ${duration}ms`, data || '');
    }

    userAction(action, data = null) {
        const logEntry = this._formatMessage('info', `User Action: ${action}`, data);
        console.log(`[USER][${logEntry.source}] ${action}`, data || '');
        this._sendToBackend(logEntry);
    }
}

// Factory function for creating component loggers
function createLogger(component, subcomponent = null) {
    return new FrontendLogger(component, subcomponent);
}

// Global error handler
window.addEventListener('error', (event) => {
    const globalLogger = new FrontendLogger('global');
    globalLogger.error('Unhandled JavaScript error', {
        message: event.message,
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        error: event.error ? event.error.stack : null
    });
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FrontendLogger, createLogger };
}

// Make available globally
window.GremlinLogger = { FrontendLogger, createLogger };
