<template>
  <div class="about-page">
    <!-- Navbar -->
    <nav class="nav">
      <div class="nav-brand" @click="goHome">ThinkSwarm</div>
      <div class="nav-menu">
        <button class="nav-menu-btn" @click="goHome">Home</button>
        <button class="nav-menu-btn" @click="goToEngine">Engine</button>
        <button class="nav-menu-btn active">About Us</button>
      </div>
    </nav>

    <!-- Profile Area -->
    <section class="about-hero">
      <div class="profile-container">
        <div class="profile-meta">
          <span class="meta-tag">Developer Profile</span>
        </div>
        <h1 class="profile-name">Abel Yohannes</h1>
        <p class="profile-title">Computer Engineer</p>

        <div class="profile-divider"></div>

        <div class="profile-details">
          <div class="details-section">
            <h2>Background & Engineering</h2>
            <p>
              As a Computer Engineer, I design and build highly scalable, parallel architectures that bring complex mathematical systems into real-world software applications. My work focuses on systems design, database scaling, high-concurrency computation, and parallel digital environments.
            </p>
          </div>

          <div class="details-section">
            <h2>Swarm Intelligence Vision</h2>
            <p>
              ThinkSwarm represents my passion for simulating organizational behavior. By leveraging GraphRAG, entity-relationship structures, and autonomous LLM agents, I aim to provide executives and project managers with a digital rehearsal laboratory to optimize financial forecasting and ERPNext workflows before real-world execution.
            </p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}

const goToEngine = () => {
  router.push('/engine')
}
</script>

<style scoped>
/* ===== BASE ===== */
.about-page {
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

/* ===== HERO PROFILE ===== */
.about-hero {
  max-width: 800px;
  margin: 0 auto;
  padding: 100px 48px 120px;
  text-align: left;
}

.profile-container {
  display: flex;
  flex-direction: column;
}

.profile-meta {
  margin-bottom: 20px;
}

.meta-tag {
  background: var(--c-black);
  color: var(--c-white);
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  padding: 4px 10px;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.profile-name {
  font-family: var(--font-display);
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -2px;
  margin-bottom: 8px;
  color: var(--c-black);
}

.profile-title {
  font-family: var(--font-mono);
  font-size: 1.1rem;
  color: var(--c-gray-600);
  margin-bottom: 32px;
}

.profile-divider {
  height: 1px;
  background: var(--c-gray-200);
  width: 100%;
  margin-bottom: 40px;
}

.profile-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
}

.details-section h2 {
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: var(--c-black);
}

.details-section p {
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--c-gray-700);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
  .about-hero {
    padding: 60px 24px 80px;
  }

  .profile-name {
    font-size: 2.8rem;
  }

  .profile-details {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .nav {
    padding: 0 24px;
  }
}
</style>
