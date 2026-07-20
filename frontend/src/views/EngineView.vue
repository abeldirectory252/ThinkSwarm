<template>
  <div class="engine-page">
    <!-- Navbar -->
    <nav class="nav">
      <div class="nav-brand" @click="goHome">ThinkSwarm</div>
      <div class="nav-menu">
        <button class="nav-menu-btn" @click="goHome">Home</button>
        <button class="nav-menu-btn active">Engine</button>
        <button class="nav-menu-btn" @click="goToAbout">About Me</button>
      </div>
    </nav>

    <!-- Main Console / Try It -->
    <section class="try-section">
      <div class="try-header">
        <div class="tag-row">
          <span class="tag">01 / Reality Seed</span>
          <span class="status-badge">Standby</span>
        </div>
        <h2 class="try-title">Simulation Engine Setup</h2>
        <p class="try-subtitle">Upload seed data (PDF, MD, TXT format) to initialize a parallel digital twin sequence.</p>
      </div>

      <div class="try-box">
        <div class="try-columns">
          <!-- Upload -->
          <div class="try-panel">
            <div class="panel-label">
              <span>Reality Seed Materials</span>
              <span class="panel-meta">PDF, MD, TXT</span>
            </div>
            <div
              class="upload-zone"
              :class="{ 'drag-over': isDragOver, 'has-files': files.length > 0 }"
              @dragover.prevent="handleDragOver"
              @dragleave.prevent="handleDragLeave"
              @drop.prevent="handleDrop"
              @click="triggerFileInput"
            >
              <input
                ref="fileInput"
                type="file"
                multiple
                accept=".pdf,.md,.txt"
                @change="handleFileSelect"
                style="display: none"
                :disabled="loading"
              />
              <div v-if="files.length === 0" class="upload-empty">
                <div class="upload-icon">↑</div>
                <div class="upload-label">Drag files to upload</div>
                <div class="upload-hint">or click to browse files</div>
              </div>
              <div v-else class="file-list">
                <div v-for="(file, idx) in files" :key="idx" class="file-row">
                  <span>📄</span>
                  <span class="file-name">{{ file.name }}</span>
                  <button @click.stop="removeFile(idx)" class="file-remove">×</button>
                </div>
              </div>
            </div>
          </div>

          <!-- Prompt -->
          <div class="try-panel">
            <div class="panel-label">
              <span>02 / Simulation Prompt</span>
              <span class="panel-meta">System Instructions</span>
            </div>
            <div class="textarea-wrap">
              <textarea
                v-model="formData.simulationRequirement"
                class="prompt-input"
                :placeholder="$t('home.promptPlaceholder')"
                rows="6"
                :disabled="loading"
              ></textarea>
              <span class="engine-badge">{{ $t('home.engineBadge') }}</span>
            </div>
          </div>
        </div>

        <!-- Submit -->
        <button
          class="submit-btn"
          @click="startSimulation"
          :disabled="!canSubmit || loading"
        >
          <span v-if="!loading">Start Simulation</span>
          <span v-else>{{ $t('home.initializing') }}</span>
          <span class="btn-arrow">→</span>
        </button>
      </div>
    </section>

    <!-- History -->
    <HistoryDatabase />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const router = useRouter()

// Form data
const formData = ref({
  simulationRequirement: ''
})

// File list
const files = ref([])

// State
const loading = ref(false)
const isDragOver = ref(false)

// File input ref
const fileInput = ref(null)

// Computed: whether form can be submitted
const canSubmit = computed(() => {
  return formData.value.simulationRequirement.trim() !== '' && files.value.length > 0
})

// Navigation helpers
const goHome = () => {
  router.push('/')
}

const goToAbout = () => {
  router.push({ path: '/', query: { scroll: 'about' } })
}

// Trigger file selection
const triggerFileInput = () => {
  if (!loading.value) {
    fileInput.value?.click()
  }
}

// Handle file selection
const handleFileSelect = (event) => {
  const selectedFiles = Array.from(event.target.files)
  addFiles(selectedFiles)
}

// Handle drag events
const handleDragOver = (e) => {
  if (!loading.value) {
    isDragOver.value = true
  }
}

const handleDragLeave = (e) => {
  isDragOver.value = false
}

const handleDrop = (e) => {
  isDragOver.value = false
  if (loading.value) return
  
  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

// Add files
const addFiles = (newFiles) => {
  const validFiles = newFiles.filter(file => {
    const ext = file.name.split('.').pop().toLowerCase()
    return ['pdf', 'md', 'txt'].includes(ext)
  })
  files.value.push(...validFiles)
}

// Remove file
const removeFile = (index) => {
  files.value.splice(index, 1)
}

// Start simulation
const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  
  // Save files and requirements
  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(files.value, formData.value.simulationRequirement)
    
    // Navigate to Process page
    router.push({
      name: 'Process',
      params: { projectId: 'new' }
    })
  })
}
</script>

<style scoped>
/* ===== BASE ===== */
.engine-page {
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

/* ===== TRY SECTION ===== */
.try-section {
  max-width: 1000px;
  margin: 0 auto;
  padding: 80px 48px 80px;
}

.try-header {
  text-align: center;
  margin-bottom: 40px;
}

.tag-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
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

.status-badge {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--c-gray-500);
  border: 1px solid var(--c-gray-300);
  padding: 3px 8px;
  border-radius: var(--radius-sm);
}

.try-title {
  font-family: var(--font-display);
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 12px;
  letter-spacing: -1px;
}

.try-subtitle {
  font-size: 0.95rem;
  color: var(--c-gray-600);
  line-height: 1.6;
}

.try-box {
  border: 1px solid var(--c-gray-200);
  background: var(--c-white);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

.try-columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-bottom: 1px solid var(--c-gray-200);
}

.try-panel {
  padding: 24px;
}

.try-panel:first-child {
  border-right: 1px solid var(--c-gray-200);
}

.panel-label {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--c-gray-500);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 12px;
}

.panel-meta {
  color: var(--c-gray-400);
}

/* Upload */
.upload-zone {
  border: 1px dashed var(--c-gray-300);
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s var(--ease);
  background: var(--c-gray-50);
  border-radius: var(--radius-sm);
  width: 100%;
}

.upload-zone:hover {
  border-color: var(--c-black);
  background: var(--c-gray-50);
}

.upload-zone.drag-over {
  border-color: var(--c-black);
  background: var(--c-gray-100);
}

.upload-zone.has-files {
  align-items: flex-start;
  min-height: 180px;
}

.upload-empty {
  text-align: center;
  padding: 20px;
}

.upload-icon {
  width: 36px;
  height: 36px;
  border: 1px solid var(--c-gray-200);
  background: var(--c-white);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  font-size: 1.1rem;
  color: var(--c-gray-600);
  border-radius: 50%;
  transition: transform 0.2s var(--ease), border-color 0.2s var(--ease), color 0.2s var(--ease);
}

.upload-zone:hover .upload-icon {
  transform: translateY(-3px);
  border-color: var(--c-black);
  color: var(--c-black);
  box-shadow: 0 4px 10px rgba(0,0,0,0.03);
}

.upload-label {
  font-size: 0.88rem;
  font-weight: 500;
  margin-bottom: 4px;
}

.upload-hint {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--c-gray-400);
}

.file-list {
  width: 100%;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.file-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--c-white);
  border: 1px solid var(--c-gray-200);
  font-family: var(--font-mono);
  font-size: 0.82rem;
}

.file-name {
  flex: 1;
}

.file-remove {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  color: var(--c-gray-400);
  line-height: 1;
}

.file-remove:hover {
  color: var(--c-black);
}

/* Prompt */
.textarea-wrap {
  position: relative;
  border: 1px solid var(--c-gray-200);
  background: var(--c-gray-50);
  border-radius: var(--radius-sm);
  min-height: 180px;
  transition: border-color 0.2s var(--ease), box-shadow 0.2s var(--ease);
}

.textarea-wrap:focus-within {
  border-color: var(--c-black);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.04);
}

.prompt-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 16px;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  line-height: 1.7;
  resize: none;
  outline: none;
  height: 180px;
  color: var(--c-black);
}

.prompt-input::placeholder {
  color: var(--c-gray-400);
}

.engine-badge {
  position: absolute;
  bottom: 8px;
  right: 12px;
  font-family: var(--font-mono);
  font-size: 0.65rem;
  color: var(--c-gray-400);
}

/* Submit */
.submit-btn {
  width: 100%;
  background: var(--c-black);
  color: var(--c-white);
  border: none;
  padding: 18px 24px;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 0.95rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  letter-spacing: 0.5px;
  transition: all 0.2s var(--ease);
}

.submit-btn:hover:not(:disabled) {
  background: var(--c-gray-800);
}

.submit-btn:disabled {
  background: var(--c-gray-200);
  color: var(--c-gray-400);
  cursor: not-allowed;
}

.btn-arrow {
  transition: transform 0.2s var(--ease);
}

.submit-btn:hover:not(:disabled) .btn-arrow {
  transform: translateX(4px);
}

/* ===== RESPONSIVE ===== */
@media (max-width: 1024px) {
  .nav {
    padding: 0 24px;
  }

  .try-section {
    padding-left: 24px;
    padding-right: 24px;
  }
}

@media (max-width: 768px) {
  .try-columns {
    grid-template-columns: 1fr;
  }
  
  .try-panel:first-child {
    border-right: none;
    border-bottom: 1px solid var(--c-gray-200);
  }
}
</style>
