<template>
  <div class="home">
    <!-- Navbar -->
    <nav class="nav">
      <div class="nav-brand" @click="scrollToTop">ThinkSwarm</div>
      <div class="nav-menu">
        <button class="nav-menu-btn active" @click="scrollToTop">Home</button>
        <button class="nav-menu-btn" @click="goToEngine">Engine</button>
        <button class="nav-menu-btn" @click="goToAbout">About Us</button>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-text">
        <div class="tag-row">
          <span class="tag">{{ $t('home.tagline') }}</span>
          <span class="version">{{ $t('home.version') }}</span>
        </div>

        <h1 class="title">
          {{ $t('home.heroTitle1') }}<br>
          <span class="title-accent">{{ $t('home.heroTitle2') }}</span>
        </h1>

        <div class="desc">
          <p>
            <i18n-t keypath="home.heroDesc" tag="span">
              <template #brand><strong>{{ $t('home.heroDescBrand') }}</strong></template>
              <template #agentScale><span class="mono-highlight">{{ $t('home.heroDescAgentScale') }}</span></template>
              <template #optimalSolution><code class="code-tag">{{ $t('home.heroDescOptimalSolution') }}</code></template>
            </i18n-t>
          </p>
          <p class="slogan">
            {{ $t('home.slogan') }}<span class="cursor">_</span>
          </p>
        </div>

        <button class="try-btn" @click="goToEngine">
          {{ $t('home.startEngine') }} <span>→</span>
        </button>
      </div>
    </section>

    <!-- How It Works -->
    <section class="how-it-works">
      <div class="section-label">
        <span class="dot">●</span> {{ $t('home.workflowSequence') }}
      </div>

      <div class="steps-grid">
        <div class="step-card" v-for="i in 5" :key="i">
          <span class="step-number">{{ String(i).padStart(2, '0') }}</span>
          <div class="step-title">{{ $t(`home.step${String(i).padStart(2, '0')}Title`) }}</div>
          <div class="step-desc">{{ $t(`home.step${String(i).padStart(2, '0')}Desc`) }}</div>
        </div>
      </div>

      <div class="metrics">
        <div class="metric">
          <div class="metric-val">{{ $t('home.metricLowCost') }}</div>
          <div class="metric-lbl">{{ $t('home.metricLowCostDesc') }}</div>
        </div>
        <div class="metric">
          <div class="metric-val">{{ $t('home.metricHighAvail') }}</div>
          <div class="metric-lbl">{{ $t('home.metricHighAvailDesc') }}</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// Scroll functions
const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const goToEngine = () => {
  router.push('/engine')
}

const goToAbout = () => {
  router.push('/about')
}
</script>

<style scoped>
/* ===== BASE ===== */
.home {
  min-height: 100vh;
  background: var(--c-white);
  color: var(--c-black);
}

/* ===== NAV ===== */
.nav {
  height: 56px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 48px;
  border-bottom: 1px solid var(--c-gray-200);
  position: sticky;
  top: 0;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: 100;
}

.nav-brand {
  font-family: var(--font-mono);
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: 1px;
  cursor: pointer;
}

.nav-menu {
  display: flex;
  gap: 24px;
}

.nav-menu-btn {
  background: transparent;
  border: none;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--c-gray-600);
  cursor: pointer;
  padding: 4px 8px;
  transition: color 0.2s var(--ease);
}

.nav-menu-btn:hover,
.nav-menu-btn.active {
  color: var(--c-black);
  font-weight: 700;
}

/* ===== HERO ===== */
.hero {
  max-width: 800px;
  margin: 0 auto;
  padding: 100px 48px 120px;
  text-align: left;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.tag {
  background: var(--c-black);
  color: var(--c-white);
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  padding: 4px 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.version {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--c-gray-500);
}

.title {
  font-family: var(--font-display);
  font-size: 4rem;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -2px;
  margin-bottom: 32px;
  color: var(--c-black);
}

.title-accent {
  color: var(--c-gray-500);
}

.desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: var(--c-gray-600);
  max-width: 600px;
  margin-bottom: 40px;
}

.desc p {
  margin-bottom: 16px;
}

.desc strong {
  color: var(--c-black);
  font-weight: 600;
}

.mono-highlight {
  font-family: var(--font-mono);
  font-weight: 600;
  color: var(--c-black);
}

.code-tag {
  font-family: var(--font-mono);
  font-size: 0.88em;
  background: var(--c-gray-100);
  border: 1px solid var(--c-gray-200);
  padding: 1px 6px;
  border-radius: 3px;
  color: var(--c-gray-800);
}

.slogan {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--c-black);
  border-left: 2px solid var(--c-black);
  padding-left: 14px;
  margin-top: 8px;
}

.cursor {
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  50% { opacity: 0; }
}

.try-btn {
  background: var(--c-black);
  color: var(--c-white);
  border: none;
  padding: 14px 32px;
  font-family: var(--font-mono);
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  letter-spacing: 0.5px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s var(--ease);
}

.try-btn:hover {
  background: var(--c-gray-800);
  transform: translateY(-1px);
}

/* ===== HOW IT WORKS ===== */
.how-it-works {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 48px 80px;
}

.section-label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--c-gray-500);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 28px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  font-size: 0.5rem;
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1px;
  background: var(--c-gray-200);
  border: 1px solid var(--c-gray-200);
  margin-bottom: 32px;
}

.step-card {
  background: var(--c-white);
  padding: 24px 20px;
  transition: background 0.2s var(--ease);
}

.step-card:hover {
  background: var(--c-gray-50);
}

.step-number {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--c-gray-400);
  display: block;
  margin-bottom: 12px;
}

.step-card:hover .step-number {
  color: var(--c-black);
}

.step-title {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 6px;
  line-height: 1.3;
}

.step-desc {
  font-size: 0.78rem;
  color: var(--c-gray-600);
  line-height: 1.5;
}

.metrics {
  display: flex;
  gap: 1px;
  background: var(--c-gray-200);
  border: 1px solid var(--c-gray-200);
}

.metric {
  flex: 1;
  background: var(--c-white);
  padding: 24px 28px;
}

.metric-val {
  font-family: var(--font-mono);
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.metric-lbl {
  font-size: 0.8rem;
  color: var(--c-gray-500);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
  .hero {
    padding: 60px 24px 80px;
  }

  .title {
    font-size: 3rem;
  }

  .steps-grid {
    grid-template-columns: 1fr 1fr;
  }

  .nav {
    padding: 0 24px;
  }

  .how-it-works {
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (max-width: 640px) {
  .steps-grid {
    grid-template-columns: 1fr;
  }

  .metrics {
    flex-direction: column;
  }
}
</style>

<style>
/* English locale adjustments */
html[lang="en"] .title {
  font-size: 3.4rem;
  letter-spacing: -1.5px;
}

html[lang="en"] .desc {
  font-family: var(--font-body);
}

html[lang="en"] .slogan {
  font-family: var(--font-body);
}

html[lang="en"] .step-desc {
  font-size: 0.72rem;
  line-height: 1.4;
}
</style>
