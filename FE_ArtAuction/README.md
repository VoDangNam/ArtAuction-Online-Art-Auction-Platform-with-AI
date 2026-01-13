# **ART AUCTION FRONTEND - INSTALLATION GUIDE**

PROJECT INFORMATION
------------------
Project Name: FE_ArtAuction
Version: 0.0.0
Framework: Vue 3 with Vite
Type: Frontend Application for Online Art Auction Platform

SYSTEM REQUIREMENTS

- Node.js: Version ^20.19.0 or >=22.12.0
  Download from: https://nodejs.org/

- npm: Comes with Node.js (or use yarn/pnpm as alternative)

- Git: For version control (if cloning from repository)
  Download from: https://git-scm.com/

INSTALLATION STEPS

STEP 1: Install Node.js
------------------------
1. Visit https://nodejs.org/
2. Download and install Node.js version 20.19.0 or higher
3. Verify installation by opening terminal/command prompt:
   node --version
   npm --version

STEP 2: Clone or Download Project
----------------------------------
If using Git:
   git clone [repository-url]
   cd FE_ArtAuction

Or extract the project folder to your desired location.

STEP 3: Install Dependencies
------------------------------
1. Open terminal/command prompt in the project root directory
2. Navigate to project folder (if not already there):
   
   cd FE_ArtAuction

3. Install all dependencies at once:
   
   npm install
   
   OR use shorthand:
   
   npm i

   This will install all required packages listed in package.json
   Installation may take a few minutes depending on your internet speed.
   
   Expected output:
   - Creates node_modules/ folder with all packages
   - Creates package-lock.json file (locks dependency versions)
   - Shows installation progress and any warnings

4. If installation fails, try:
   
   npm cache clean --force
   npm install
   
   Or delete node_modules and package-lock.json, then reinstall:
   
   rm -rf node_modules package-lock.json  (Linux/Mac)
   rmdir /s node_modules & del package-lock.json  (Windows)
   npm install

STEP 4: Configure Environment (if needed)
------------------------------------------
1. Check if there's a .env file or .env.example file in the root directory
2. If .env.example exists, copy it to create .env:
   
   cp .env.example .env  (Linux/Mac)
   copy .env.example .env  (Windows)

3. Configure the following in .env file (if needed):
   - API_BASE_URL=http://localhost:8081/api
   - WEBSOCKET_URL=ws://localhost:8081/ws
   - ZEGOCLOUD_APP_ID=your_app_id
   - ZEGOCLOUD_APP_SECRET=your_app_secret
   
4. Contact the backend team for API configuration details
5. Never commit .env file to version control (should be in .gitignore)

STEP 5: Run Development Server
--------------------------------
After installation is complete, run:

   npm run dev
   
   OR:
   
   npm run dev -- --host  (to allow access from other devices on network)
   npm run dev -- --port 3000  (to use a different port)

The application will start on a local development server.
Default URL: http://localhost:5173

You should see output like:
   VITE v7.0.6  ready in 500 ms
   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose

Open your browser and navigate to the displayed URL.
The page will automatically reload when you make changes to the code.

AVAILABLE SCRIPTS

npm run dev
-----------
Starts the development server with hot-reload.
The application will automatically reload when you make changes to the code.
Default URL: http://localhost:5173

npm run build
-------------
Builds the application for production.
Creates an optimized production build in the 'dist' folder.
Use this before deploying to a production server.

npm run preview
---------------
Previews the production build locally.
Run this after 'npm run build' to test the production version.

npm run lint
------------
Runs ESLint to check and fix code quality issues.
Automatically fixes auto-fixable problems.

TOOLS AND DEPENDENCIES - DETAILED INSTALLATION GUIDE

NOTE: All packages are already listed in package.json. 
      Run "npm install" to install all at once.
      Or install individually using the commands below.

CORE FRAMEWORK & BUILD TOOLS

1. Vue 3.5.18
   Description: Progressive JavaScript framework for building user interfaces
   Installation Command:
      npm install vue
   
   Website: https://vuejs.org/
   Documentation: https://vuejs.org/guide/


2. Vite 7.0.6
   Description: Next-generation frontend build tool, provides fast development
   Installation Command:
      npm install --save-dev vite
   
   Website: https://vite.dev/
   Documentation: https://vite.dev/guide/


3. Vue Router 4.0.13
   Description: Official router for Vue.js, handles navigation and routing
   Installation Command:
      npm install vue-router
   
   Website: https://router.vuejs.org/
   Documentation: https://router.vuejs.org/guide/


UI FRAMEWORK & STYLING

4. Bootstrap 5.3.8
   Description: Popular CSS framework for responsive design
   Installation Command:
      npm install bootstrap
   
   Website: https://getbootstrap.com/
   Documentation: https://getbootstrap.com/docs/5.3/


5. Bootstrap Icons 1.13.1
   Description: Icon library for Bootstrap
   Installation Command:
      npm install bootstrap-icons
   
   Website: https://icons.getbootstrap.com/
   Documentation: https://icons.getbootstrap.com/


6. Font Awesome 7.0.1
   Description: Icon library and toolkit
   Installation Command:
      npm install @fortawesome/fontawesome-free
   
   Website: https://fontawesome.com/
   Documentation: https://fontawesome.com/docs


7. AOS (Animate On Scroll) 2.3.4
   Description: Library for scroll animations
   Installation Command:
      npm install aos
   
   Website: https://michalsnik.github.io/aos/
   Documentation: https://michalsnik.github.io/aos/


HTTP CLIENT & API

8. Axios 1.12.2
   Description: Promise-based HTTP client for making API requests
   Installation Command:
      npm install axios
   
   Usage Example:
      import axios from 'axios'
      axios.get('/api/endpoint')
   
   Website: https://axios-http.com/
   Documentation: https://axios-http.com/docs/intro


REAL-TIME COMMUNICATION

9. @stomp/stompjs 7.2.1
   Description: STOMP client for WebSocket communication
   Used for: Real-time auction updates and chat
   Installation Command:
      npm install @stomp/stompjs
   
   Usage Example:
      import { Client } from '@stomp/stompjs'
      const client = new Client()
   
   Website: https://stomp-js.github.io/
   Documentation: https://stomp-js.github.io/api-docs/latest/


10. sockjs-client 1.6.1
    Description: WebSocket-like object for real-time communication
    Installation Command:
       npm install sockjs-client
    
    Website: https://www.npmjs.com/package/sockjs-client
    Documentation: https://github.com/sockjs/sockjs-client


LIVE STREAMING

11. @zegocloud/zego-uikit-prebuilt 2.17.0
    Description: Pre-built UI kit for ZegoCloud live streaming
    Used for: Auction room live streaming features
    Installation Command:
       npm install @zegocloud/zego-uikit-prebuilt
    
    Website: https://www.zegocloud.com/
    Documentation: https://docs.zegocloud.com/article/14746


NOTIFICATIONS

12. @meforma/vue-toaster 1.3.0
    Description: Toast notification component for Vue 3
    Used for: Displaying success/error messages
    Installation Command:
       npm install @meforma/vue-toaster
    
    Usage Example:
       import { createToaster } from '@meforma/vue-toaster'
       const toaster = createToaster()
       toaster.success('Success message')
    
    Website: https://www.npmjs.com/package/@meforma/vue-toaster
    Documentation: https://github.com/meforma/vue-toaster


CHARTS & DATA VISUALIZATION

13. Chart.js 4.5.1
    Description: JavaScript charting library
    Used for: Displaying statistics and analytics
    Installation Command:
       npm install chart.js
    
    Usage Example:
       import { Chart } from 'chart.js'
    
    Website: https://www.chartjs.org/
    Documentation: https://www.chartjs.org/docs/latest/


UTILITIES

14. jQuery 3.7.1
    Description: JavaScript library for DOM manipulation
    Installation Command:
       npm install jquery
    
    Website: https://jquery.com/
    Documentation: https://api.jquery.com/


DEVELOPMENT TOOLS (DevDependencies)

15. ESLint 9.31.0
    Description: JavaScript linter for code quality
    Installation Command:
       npm install --save-dev eslint
    
    Website: https://eslint.org/
    Documentation: https://eslint.org/docs/latest/


16. eslint-plugin-vue 10.3.0
    Description: ESLint plugin for Vue.js files
    Installation Command:
       npm install --save-dev eslint-plugin-vue
    
    Website: https://eslint.vuejs.org/
    Documentation: https://eslint.vuejs.org/user-guide/


17. @vitejs/plugin-vue 6.0.1
    Description: Vite plugin for Vue.js support
    Installation Command:
       npm install --save-dev @vitejs/plugin-vue
    
    Website: https://vite.dev/
    Documentation: https://vite.dev/guide/


18. vite-plugin-vue-devtools 8.0.0
    Description: Vue DevTools integration for Vite
    Installation Command:
       npm install --save-dev vite-plugin-vue-devtools
    
    Website: https://www.npmjs.com/package/vite-plugin-vue-devtools
    Documentation: https://github.com/webfansplz/vite-plugin-vue-devtools


19. sass-embedded 1.93.3
    Description: Sass compiler for CSS preprocessing
    Installation Command:
       npm install --save-dev sass-embedded
    
    Website: https://sass-lang.com/
    Documentation: https://sass-lang.com/documentation/


INSTALLATION COMMANDS SUMMARY

INSTALL ALL DEPENDENCIES AT ONCE:
---------------------------------
   npm install

   This installs all packages listed in package.json automatically.


INSTALL INDIVIDUAL PACKAGES:
----------------------------
   # Core Framework
   npm install vue
   npm install vue-router
   
   # UI Framework
   npm install bootstrap
   npm install bootstrap-icons
   npm install @fortawesome/fontawesome-free
   npm install aos
   
   # HTTP Client
   npm install axios
   
   # Real-time Communication
   npm install @stomp/stompjs
   npm install sockjs-client
   
   # Live Streaming
   npm install @zegocloud/zego-uikit-prebuilt
   
   # Notifications
   npm install @meforma/vue-toaster
   
   # Charts
   npm install chart.js
   
   # Utilities
   npm install jquery
   
   # Development Tools (use --save-dev flag)
   npm install --save-dev vite
   npm install --save-dev eslint
   npm install --save-dev eslint-plugin-vue
   npm install --save-dev @vitejs/plugin-vue
   npm install --save-dev vite-plugin-vue-devtools
   npm install --save-dev sass-embedded


UPDATE PACKAGES:
---------------
   # Update all packages to latest versions
   npm update
   
   # Update specific package
   npm update axios
   
   # Update to latest major version (use with caution)
   npm install axios@latest


REMOVE PACKAGES:
---------------
   # Remove a package
   npm uninstall axios
   
   # Remove a dev dependency
   npm uninstall --save-dev eslint


CHECK INSTALLED PACKAGES:
-----------------------
   # List all installed packages
   npm list
   
   # List only top-level packages
   npm list --depth=0
   
   # Check for outdated packages
   npm outdated
   
   # Check package information
   npm info axios

PROJECT STRUCTURE

FE_ArtAuction/
├── public/                 # Static assets served as-is
│   ├── HopDong_ArtAuction.html
│   ├── QuyChe_ArtAuction.html
│   └── terms-of-service.html
├── src/
│   ├── assets/            # Images, CSS, JS files
│   ├── components/        # Reusable Vue components
│   ├── composables/       # Vue composables (reusable logic)
│   ├── layout/            # Layout components (Admin/Client)
│   ├── router/            # Vue Router configuration
│   ├── services/          # API service files
│   ├── views/             # Page components
│   │   ├── Admin/         # Admin panel pages
│   │   ├── Client/        # Client/user pages
│   │   └── Khachhang/     # Guest pages
│   ├── App.vue           # Root component
│   ├── main.js           # Application entry point
│   └── socket.js         # WebSocket configuration
├── package.json          # Project dependencies and scripts
├── vite.config.js        # Vite configuration
└── README.txt           # This file

TROUBLESHOOTING

ISSUE: "node: command not found" or "npm: command not found"
SOLUTION: Make sure Node.js is installed and added to your system PATH.

ISSUE: "npm install" fails with errors
SOLUTION: 
1. Delete node_modules folder and package-lock.json:
   
   Windows:
      rmdir /s /q node_modules
      del package-lock.json
   
   Linux/Mac:
      rm -rf node_modules package-lock.json

2. Clear npm cache:
      npm cache clean --force

3. Verify Node.js and npm versions:
      node --version  (should be ^20.19.0 or >=22.12.0)
      npm --version

4. Try installing again:
      npm install

5. If still failing, try:
      npm install --legacy-peer-deps
   
   Or use yarn instead:
      npm install -g yarn
      yarn install

ISSUE: Port 5173 already in use
SOLUTION:
- Close other applications using that port, or
- Configure Vite to use a different port in vite.config.js

ISSUE: Module not found errors
SOLUTION:
1. Make sure all dependencies are installed:
      npm install

2. Check if the import path is correct:
   - Use relative paths: import Component from './components/Component.vue'
   - Use absolute paths: import Component from '@/components/Component.vue'
   - Check jsconfig.json or vite.config.js for path aliases

3. Verify the file exists in the specified location

4. If a specific package is missing:
      npm install [package-name]
   
   Example:
      npm install axios

5. Restart the development server after installing new packages:
      npm run dev

6. Clear Vite cache:
      Delete .vite folder (if exists)
      npm run dev

ISSUE: CORS errors when calling API
SOLUTION:
- Configure CORS on the backend server
- Or use a proxy configuration in vite.config.js

ISSUE: WebSocket connection fails
SOLUTION:
- Verify the WebSocket server URL is correct
- Check if the backend WebSocket server is running
- Verify firewall/network settings

ADDITIONAL NOTES

- The application uses Vue 3 Composition API
- State management: Currently using component-level state (consider Vuex/Pinia for complex state)
- Authentication: Implemented via router guards (checkAdmin.js, checkUser.js)
- API Base URL: Configure in axios instance or environment variables
- WebSocket: Configured in socket.js for real-time features
- Styling: Uses Bootstrap 5 with custom CSS overrides
  

