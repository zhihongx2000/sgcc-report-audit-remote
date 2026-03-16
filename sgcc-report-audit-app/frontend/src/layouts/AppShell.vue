<script setup lang="ts">
import { computed } from "vue";
import { RouterLink, RouterView, useRoute } from "vue-router";

import EmptyState from "../components/common/EmptyState.vue";

type NavItem = {
  path: string;
  label: string;
  icon: string;
};

const navItems: NavItem[] = [
  { path: "/audit-results", label: "报告审查", icon: "◆" },
  { path: "/overview", label: "系统总览", icon: "◉" },
  { path: "/data-browser", label: "数据浏览器", icon: "▣" },
  { path: "/ingestion-manager", label: "Ingestion管理", icon: "◍" },
  { path: "/ingestion-traces", label: "Ingestion追踪", icon: "◎" },
  { path: "/query-traces", label: "Query追踪", icon: "◈" },
  { path: "/evaluation", label: "评估面板", icon: "◌" },
];

const topTabs = [
  "报告审查",
  "系统总览",
  "数据浏览器",
  "Ingestion管理",
  "Ingestion追踪",
  "Query追踪",
  "评估面板",
];

const route = useRoute();

const activeLabel = computed(() => {
  const current = navItems.find((item) => item.path === route.path);
  return current?.label ?? "系统总览";
});

const breadcrumbText = computed(() => `Dashboard / ${activeLabel.value}`);
</script>

<template>
  <div class="app-shell">
    <header class="global-topbar">
      <div class="brand-line">
        <p class="brand-mark">⚡ 电能质量报告审查系统 Dashboard</p>
        <nav aria-label="Top navigation" class="top-tabs">
          <span v-for="tab in topTabs" :key="tab" class="top-tab">{{
            tab
          }}</span>
        </nav>
      </div>
      <div class="topbar-tools">
        <label class="search-pill">
          <span class="search-icon">⌕</span>
          <input
            aria-label="search"
            placeholder="搜索报告、文档、Trace"
            type="text"
          />
        </label>
        <div class="user-badge">管理员</div>
      </div>
    </header>

    <div class="workspace">
      <aside class="side-menu" aria-label="Sidebar navigation">
        <p class="side-title">功能菜单</p>
        <nav class="side-nav">
          <RouterLink
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="side-link"
            active-class="is-active"
          >
            <span aria-hidden="true" class="link-icon">{{ item.icon }}</span>
            <span>{{ item.label }}</span>
          </RouterLink>
        </nav>
      </aside>

      <div class="workspace-main">
        <header class="page-bar">
          <p class="page-title">{{ activeLabel }}</p>
          <p class="breadcrumb" :title="breadcrumbText">{{ breadcrumbText }}</p>
        </header>

        <main class="page-content">
          <RouterView v-slot="{ Component }">
            <component :is="Component" v-if="Component" />
            <EmptyState
              v-else
              title="页面建设中"
              description="当前路由尚未绑定页面组件。"
            />
          </RouterView>
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: radial-gradient(
      circle at 12% -14%,
      rgba(69, 123, 188, 0.46) 0%,
      transparent 48%
    ),
    linear-gradient(
      180deg,
      var(--color-brand-800) 0%,
      var(--color-brand-900) 36%,
      var(--color-bg-canvas) 36%
    );
  color: var(--color-text-primary);
  font-family: var(--font-body);
  overflow-x: hidden;
}

.global-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  padding: 0.68rem 1.15rem;
  background: linear-gradient(
    92deg,
    var(--color-brand-900) 0%,
    var(--color-brand-800) 54%,
    #1f4f8f 100%
  );
  color: var(--color-text-inverse);
  box-shadow: var(--shadow-medium);
  position: sticky;
  top: 0;
  z-index: 30;
}

.brand-line {
  display: flex;
  align-items: center;
  gap: 1.4rem;
  min-width: 0;
}

.brand-mark {
  margin: 0;
  font-family: var(--font-display);
  font-size: 1.08rem;
  letter-spacing: 0.02em;
  white-space: nowrap;
}

.top-tabs {
  display: flex;
  gap: 0.9rem;
  min-width: 0;
}

.top-tab {
  padding: 0.22rem 0.14rem;
  font-size: var(--text-md);
  color: rgba(230, 243, 255, 0.88);
  white-space: nowrap;
  border-bottom: 2px solid transparent;
  transition:
    border-color var(--duration-normal) var(--ease-standard),
    color var(--duration-normal) var(--ease-standard);
}

.top-tab:hover {
  color: #ffffff;
  border-bottom-color: var(--color-brand-300);
}

.topbar-tools {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-shrink: 0;
}

.search-pill {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.28rem 0.55rem;
  border-radius: var(--radius-pill);
  background: rgba(5, 26, 55, 0.4);
  border: 1px solid rgba(153, 196, 255, 0.42);
  min-width: min(280px, 36vw);
}

.search-icon {
  font-size: 0.86rem;
  opacity: 0.8;
}

.search-pill input {
  all: unset;
  color: var(--color-text-inverse);
  font-size: var(--text-sm);
  width: 100%;
}

.search-pill input::placeholder {
  color: rgba(219, 236, 255, 0.68);
}

.user-badge {
  padding: 0.34rem 0.8rem;
  border-radius: var(--radius-pill);
  background: rgba(223, 237, 255, 0.2);
  border: 1px solid rgba(222, 236, 255, 0.44);
  font-size: var(--text-sm);
  white-space: nowrap;
}

.workspace {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  gap: var(--space-4);
  padding: var(--space-4);
  background: var(--color-bg-surface);
  min-height: calc(100vh - 58px);
  box-sizing: border-box;
}

.side-menu {
  background: var(--color-bg-panel);
  border: 1px solid var(--color-border-soft);
  border-radius: var(--radius-lg);
  padding: 0.95rem 0.8rem;
  box-shadow: var(--shadow-soft);
  height: fit-content;
  position: sticky;
  top: 74px;
}

.side-title {
  margin: 0 0 0.72rem;
  font-weight: var(--weight-bold);
  font-size: var(--text-md);
  color: #304862;
}

.side-nav {
  display: grid;
  gap: 0.28rem;
}

.side-link {
  display: flex;
  align-items: center;
  gap: 0.52rem;
  padding: 0.55rem 0.55rem;
  text-decoration: none;
  color: #29425e;
  border-radius: var(--radius-md);
  border: 1px solid transparent;
  font-size: var(--text-md);
  transition:
    background-color var(--duration-normal) var(--ease-standard),
    transform var(--duration-fast) var(--ease-standard),
    border-color var(--duration-normal) var(--ease-standard);
}

.side-link:hover {
  background: #e4efff;
  border-color: var(--color-brand-200);
  transform: translateX(2px);
}

.side-link.is-active {
  background: linear-gradient(90deg, #e2eeff 0%, #edf4ff 100%);
  border-color: var(--color-brand-300);
  box-shadow: inset 4px 0 0 var(--color-brand-700);
  font-weight: var(--weight-bold);
}

.link-icon {
  font-size: var(--text-xs);
  color: #5a80ad;
  flex-shrink: 0;
}

.workspace-main {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  min-width: 0;
  gap: var(--space-3);
}

.page-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.6rem;
  background: var(--color-bg-panel);
  border: 1px solid var(--color-border-soft);
  border-radius: var(--radius-md);
  padding: 0.84rem 1rem;
  box-shadow: var(--shadow-soft);
}

.page-title {
  margin: 0;
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: #1f3651;
}

.breadcrumb {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.page-content {
  min-width: 0;
  overflow-x: hidden;
}

.page-content :deep(section) {
  background: var(--color-bg-panel);
  border: 1px solid var(--color-border-soft);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  box-shadow: var(--shadow-soft);
  box-sizing: border-box;
  animation: page-enter var(--duration-slow) var(--ease-standard);
}

@media (max-width: 1180px) {
  .top-tabs {
    display: none;
  }

  .search-pill {
    min-width: 210px;
  }
}

@media (max-width: 940px) {
  .workspace {
    grid-template-columns: 1fr;
    padding: 0.8rem;
  }

  .side-menu {
    position: static;
  }

  .side-nav {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  .side-link {
    justify-content: center;
    padding: 0.48rem 0.3rem;
    font-size: 0.8rem;
  }

  .side-link .link-icon {
    display: none;
  }
}

@media (max-width: 700px) {
  .global-topbar {
    padding: 0.6rem 0.72rem;
  }

  .brand-mark {
    font-size: 0.85rem;
  }

  .search-pill {
    display: none;
  }

  .side-nav {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .page-bar {
    padding: 0.7rem 0.82rem;
  }

  .breadcrumb {
    font-size: 0.77rem;
  }
}

@media (max-width: 470px) {
  .user-badge {
    font-size: 0.74rem;
    padding: 0.26rem 0.56rem;
  }

  .side-nav {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
