<template>
  <router-view />
</template>

<script setup>
// Use Vue Router for page routing
</script>

<style>
/* Global style reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  /* Strict B&W Neutral Palette */
  --c-black: #111111;
  --c-white: #FAF9F6;
  --c-gray-50: #F4F3F0;
  --c-gray-100: #EAEAE6;
  --c-gray-200: #DFDFD9;
  --c-gray-300: #CCCCCC;
  --c-gray-400: #AAAAAA;
  --c-gray-500: #888888;
  --c-gray-600: #666666;
  --c-gray-700: #444444;
  --c-gray-800: #222222;
  --c-gray-900: #111111;

  /* Claude Brand Fonts */
  --font-mono: 'JetBrains Mono', 'SF Mono', 'Fira Code', monospace;
  --font-display: 'Lora', Georgia, serif;
  --font-body: 'Outfit', 'Inter', system-ui, -apple-system, sans-serif;

  /* Spacing & Borders */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 18px;

  /* Transitions */
  --ease: cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

#app {
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--c-black);
  background-color: var(--c-white);
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: var(--c-gray-300);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--c-gray-400);
}

button {
  font-family: inherit;
}
</style>
