import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";

import AuditResultView from "../views/AuditResultView.vue";
import DataBrowserView from "../views/DataBrowserView.vue";
import EvaluationPanelView from "../views/EvaluationPanelView.vue";
import IngestionManagerView from "../views/IngestionManagerView.vue";
import IngestionTracesView from "../views/IngestionTracesView.vue";
import OverviewView from "../views/OverviewView.vue";
import QueryTracesView from "../views/QueryTracesView.vue";

export const routes: RouteRecordRaw[] = [
	{
		path: "/",
		redirect: "/audit-results",
	},
	{
		path: "/audit-results",
		name: "audit-results",
		component: AuditResultView,
	},
	{
		path: "/overview",
		name: "overview",
		component: OverviewView,
	},
	{
		path: "/data-browser",
		name: "data-browser",
		component: DataBrowserView,
	},
	{
		path: "/ingestion-manager",
		name: "ingestion-manager",
		component: IngestionManagerView,
	},
	{
		path: "/ingestion-traces",
		name: "ingestion-traces",
		component: IngestionTracesView,
	},
	{
		path: "/query-traces",
		name: "query-traces",
		component: QueryTracesView,
	},
	{
		path: "/evaluation",
		name: "evaluation",
		component: EvaluationPanelView,
	},
	{
		path: "/:pathMatch(.*)*",
		redirect: "/audit-results",
	},
];

export const router = createRouter({
	history: createWebHistory(),
	routes,
});
