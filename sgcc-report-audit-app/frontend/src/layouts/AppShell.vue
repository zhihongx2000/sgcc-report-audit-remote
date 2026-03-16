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
					<span v-for="tab in topTabs" :key="tab" class="top-tab">{{ tab }}</span>
				</nav>
			</div>
			<div class="topbar-tools">
				<label class="search-pill">
					<span class="search-icon">⌕</span>
					<input aria-label="search" placeholder="搜索报告、文档、Trace" type="text" />
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
@import url("https://fonts.googleapis.com/css2?family=Aldrich&family=Noto+Sans+SC:wght@400;500;700&display=swap");

.app-shell {
	--blue-900: #0f3268;
	--blue-800: #1b457f;
	--blue-700: #2a5a9b;
	--ink-900: #1f2c40;
	--ink-600: #5f6f84;
	--paper: #f2f5fb;
	--card: #ffffff;
	--line: #dbe4f2;
	--accent: #2db6c3;
	--danger: #dd4f64;
	min-height: 100vh;
	background: radial-gradient(circle at 8% -20%, #3d74b7 0%, #173a70 34%, #142f59 58%, #eef3fb 58%);
	color: var(--ink-900);
	font-family: "Noto Sans SC", "PingFang SC", sans-serif;
	overflow-x: hidden;
}

.global-topbar {
	display: flex;
	justify-content: space-between;
	align-items: center;
	gap: 1rem;
	padding: 0.68rem 1.15rem;
	background: linear-gradient(90deg, #143a71 0%, #1f4b86 52%, #17396f 100%);
	color: #ebf4ff;
	box-shadow: 0 12px 24px rgba(5, 22, 48, 0.28);
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
	font-family: "Aldrich", "Noto Sans SC", sans-serif;
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
	font-size: 0.9rem;
	color: rgba(230, 243, 255, 0.88);
	white-space: nowrap;
	border-bottom: 2px solid transparent;
	transition: border-color 0.2s ease, color 0.2s ease;
}

.top-tab:hover {
	color: #ffffff;
	border-bottom-color: #8fc8ff;
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
	border-radius: 999px;
	background: rgba(5, 26, 55, 0.4);
	border: 1px solid rgba(153, 196, 255, 0.32);
	min-width: min(280px, 36vw);
}

.search-icon {
	font-size: 0.86rem;
	opacity: 0.8;
}

.search-pill input {
	all: unset;
	color: #e8f2ff;
	font-size: 0.83rem;
	width: 100%;
}

.search-pill input::placeholder {
	color: rgba(214, 233, 255, 0.68);
}

.user-badge {
	padding: 0.34rem 0.8rem;
	border-radius: 999px;
	background: rgba(223, 237, 255, 0.2);
	border: 1px solid rgba(222, 236, 255, 0.44);
	font-size: 0.82rem;
	white-space: nowrap;
}

.workspace {
	display: grid;
	grid-template-columns: 240px minmax(0, 1fr);
	gap: 1rem;
	padding: 1rem;
	background: var(--paper);
	min-height: calc(100vh - 58px);
	box-sizing: border-box;
}

.side-menu {
	background: var(--card);
	border: 1px solid var(--line);
	border-radius: 14px;
	padding: 0.95rem 0.8rem;
	box-shadow: 0 10px 24px rgba(16, 38, 69, 0.08);
	height: fit-content;
	position: sticky;
	top: 74px;
}

.side-title {
	margin: 0 0 0.72rem;
	font-weight: 700;
	font-size: 0.92rem;
	color: #374a64;
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
	color: #314763;
	border-radius: 10px;
	border: 1px solid transparent;
	font-size: 0.91rem;
	transition: background-color 0.2s ease, transform 0.2s ease, border-color 0.2s ease;
}

.side-link:hover {
	background: #eaf2ff;
	border-color: #d4e4ff;
	transform: translateX(2px);
}

.side-link.is-active {
	background: linear-gradient(90deg, #e6f0ff 0%, #ecf5ff 100%);
	border-color: #c5dafb;
	box-shadow: inset 4px 0 0 #427bcc;
	font-weight: 700;
}

.link-icon {
	font-size: 0.68rem;
	color: #597ea7;
	flex-shrink: 0;
}

.workspace-main {
	display: grid;
	grid-template-rows: auto minmax(0, 1fr);
	min-width: 0;
	gap: 0.8rem;
}

.page-bar {
	display: flex;
	justify-content: space-between;
	align-items: center;
	gap: 0.6rem;
	background: #ffffff;
	border: 1px solid var(--line);
	border-radius: 12px;
	padding: 0.84rem 1rem;
	box-shadow: 0 8px 18px rgba(17, 39, 71, 0.06);
}

.page-title {
	margin: 0;
	font-size: 1rem;
	font-weight: 700;
	color: #22344d;
}

.breadcrumb {
	margin: 0;
	font-size: 0.85rem;
	color: #6b7d94;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.page-content {
	min-width: 0;
	overflow-x: hidden;
}

.page-content :deep(section) {
	background: var(--card);
	border: 1px solid var(--line);
	border-radius: 14px;
	padding: 1rem;
	box-shadow: 0 10px 24px rgba(16, 38, 69, 0.07);
	box-sizing: border-box;
	animation: content-rise 0.3s ease;
}

@keyframes content-rise {
	from {
		opacity: 0;
		transform: translateY(10px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
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
