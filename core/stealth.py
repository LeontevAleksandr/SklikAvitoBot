"""
Anti-detection техники для обхода защиты
"""

STEALTH_SCRIPT = """
// Переопределяем webdriver
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});

// Удаляем webdriver из прототипа
delete Object.getPrototypeOf(navigator).webdriver;

// Добавляем chrome объект с реалистичными свойствами
window.chrome = {
    runtime: {
        OnInstalledReason: {
            CHROME_UPDATE: "chrome_update",
            INSTALL: "install",
            SHARED_MODULE_UPDATE: "shared_module_update",
            UPDATE: "update"
        },
        OnRestartRequiredReason: {
            APP_UPDATE: "app_update",
            OS_UPDATE: "os_update",
            PERIODIC: "periodic"
        },
        PlatformArch: {
            ARM: "arm",
            ARM64: "arm64",
            MIPS: "mips",
            MIPS64: "mips64",
            X86_32: "x86-32",
            X86_64: "x86-64"
        },
        PlatformNaclArch: {
            ARM: "arm",
            MIPS: "mips",
            MIPS64: "mips64",
            X86_32: "x86-32",
            X86_64: "x86-64"
        },
        PlatformOs: {
            ANDROID: "android",
            CROS: "cros",
            LINUX: "linux",
            MAC: "mac",
            OPENBSD: "openbsd",
            WIN: "win"
        },
        RequestUpdateCheckStatus: {
            NO_UPDATE: "no_update",
            THROTTLED: "throttled",
            UPDATE_AVAILABLE: "update_available"
        }
    },
    loadTimes: function() {
        return {
            commitLoadTime: Date.now() / 1000 - Math.random() * 2,
            connectionInfo: "h2",
            finishDocumentLoadTime: Date.now() / 1000 - Math.random(),
            finishLoadTime: Date.now() / 1000 - Math.random() * 0.5,
            firstPaintAfterLoadTime: Date.now() / 1000 - Math.random() * 0.3,
            firstPaintTime: Date.now() / 1000 - Math.random() * 1.5,
            navigationType: "Other",
            npnNegotiatedProtocol: "h2",
            requestTime: Date.now() / 1000 - Math.random() * 3,
            startLoadTime: Date.now() / 1000 - Math.random() * 2.5,
            wasAlternateProtocolAvailable: false,
            wasFetchedViaSpdy: true,
            wasNpnNegotiated: true
        };
    },
    csi: function() {
        return {
            onloadT: Date.now(),
            pageT: Math.random() * 1000,
            startE: Date.now() - Math.random() * 5000,
            tran: 15
        };
    },
    app: {
        isInstalled: false,
        InstallState: {
            DISABLED: "disabled",
            INSTALLED: "installed",
            NOT_INSTALLED: "not_installed"
        },
        RunningState: {
            CANNOT_RUN: "cannot_run",
            READY_TO_RUN: "ready_to_run",
            RUNNING: "running"
        }
    }
};

// Переопределяем plugins с реалистичными данными
Object.defineProperty(navigator, 'plugins', {
    get: () => {
        const pluginArray = [
            {
                0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                description: "Portable Document Format",
                filename: "internal-pdf-viewer",
                length: 1,
                name: "Chrome PDF Plugin"
            },
            {
                0: {type: "application/pdf", suffixes: "pdf", description: ""},
                description: "",
                filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                length: 1,
                name: "Chrome PDF Viewer"
            },
            {
                0: {type: "application/pdf", suffixes: "pdf", description: "Portable Document Format"},
                description: "Portable Document Format",
                filename: "internal-pdf-viewer",
                length: 1,
                name: "WebKit built-in PDF"
            }
        ];
        pluginArray.item = function(index) { return this[index] || null; };
        pluginArray.namedItem = function(name) { 
            return this.find(p => p.name === name) || null; 
        };
        pluginArray.refresh = function() {};
        return pluginArray;
    }
});

// Переопределяем mimeTypes
Object.defineProperty(navigator, 'mimeTypes', {
    get: () => {
        const mimeArray = [
            {type: "application/pdf", suffixes: "pdf", description: "Portable Document Format"},
            {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"}
        ];
        mimeArray.item = function(index) { return this[index] || null; };
        mimeArray.namedItem = function(name) {
            return this.find(m => m.type === name) || null;
        };
        return mimeArray;
    }
});

// Переопределяем languages
Object.defineProperty(navigator, 'languages', {
    get: () => ['ru-RU', 'ru', 'en-US', 'en']
});

// Переопределяем permissions
const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) => (
    parameters.name === 'notifications' ?
        Promise.resolve({ state: Notification.permission }) :
        originalQuery(parameters)
);

// Переопределяем getBattery
if (navigator.getBattery) {
    navigator.getBattery = () => Promise.resolve({
        charging: Math.random() > 0.5,
        chargingTime: 0,
        dischargingTime: Infinity,
        level: 0.8 + Math.random() * 0.2,
        addEventListener: () => {},
        removeEventListener: () => {},
        dispatchEvent: () => true
    });
}

// Переопределяем connection
Object.defineProperty(navigator, 'connection', {
    get: () => ({
        effectiveType: '4g',
        rtt: 50 + Math.floor(Math.random() * 100),
        downlink: 5 + Math.random() * 10,
        saveData: false,
        addEventListener: () => {},
        removeEventListener: () => {},
        dispatchEvent: () => true
    })
});

// Маскируем platform
Object.defineProperty(navigator, 'platform', {
    get: () => 'Win32'
});

// Маскируем vendor
Object.defineProperty(navigator, 'vendor', {
    get: () => 'Google Inc.'
});

// Добавляем реалистичное разрешение экрана
Object.defineProperty(screen, 'availWidth', {
    get: () => window.screen.width
});
Object.defineProperty(screen, 'availHeight', {
    get: () => window.screen.height
});

// Переопределяем hardwareConcurrency на реалистичное значение
Object.defineProperty(navigator, 'hardwareConcurrency', {
    get: () => 4 + Math.floor(Math.random() * 4)
});

// Переопределяем deviceMemory
Object.defineProperty(navigator, 'deviceMemory', {
    get: () => 8
});

// Canvas fingerprint - добавляем шум
const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function() {
    const context = this.getContext('2d');
    if (context) {
        const imageData = context.getImageData(0, 0, this.width, this.height);
        for (let i = 0; i < imageData.data.length; i += 4) {
            imageData.data[i] += Math.floor(Math.random() * 3) - 1;
        }
        context.putImageData(imageData, 0, 0);
    }
    return originalToDataURL.apply(this, arguments);
};

// WebGL fingerprint - добавляем шум
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37445) {
        return 'Intel Inc.';
    }
    if (parameter === 37446) {
        return 'Intel Iris OpenGL Engine';
    }
    return getParameter.apply(this, [parameter]);
};

// AudioContext fingerprint - добавляем вариацию
const originalCreateOscillator = AudioContext.prototype.createOscillator;
AudioContext.prototype.createOscillator = function() {
    const oscillator = originalCreateOscillator.apply(this, arguments);
    const originalStart = oscillator.start;
    oscillator.start = function() {
        this.frequency.value += Math.random() * 0.001;
        return originalStart.apply(this, arguments);
    };
    return oscillator;
};

// Переопределяем Date для вариации таймингов
const originalDate = Date;
Date = class extends originalDate {
    constructor(...args) {
        if (args.length === 0) {
            super();
            this.setTime(this.getTime() + Math.floor(Math.random() * 100) - 50);
        } else {
            super(...args);
        }
    }
};
Date.now = () => originalDate.now() + Math.floor(Math.random() * 100) - 50;

// Скрываем автоматизацию в console
const originalLog = console.log;
console.log = function() {
    if (arguments[0] && arguments[0].toString().includes('puppeteer')) return;
    return originalLog.apply(this, arguments);
};
"""


async def apply_stealth(page) -> None:
    """
    Применяет anti-detection скрипты к странице
    
    Args:
        page: Объект страницы Playwright
    """
    await page.add_init_script(STEALTH_SCRIPT)