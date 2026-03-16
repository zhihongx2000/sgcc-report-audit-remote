import { createApp, h, type VNode } from "vue";

function bootstrap(): void {
	createApp({
		name: "BootstrapApp",
		setup(): () => VNode {
			return () =>
				h("main", { class: "bootstrap-app" }, [
					h("h1", "SGCC Report Audit"),
					h(
						"p",
						"Vue 3 + Vite frontend scaffold is initialized. Route and page modules will be added in subsequent tasks.",
					),
				]);
		},
	}).mount("#app");
}

bootstrap();
