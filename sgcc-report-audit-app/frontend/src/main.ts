import { createApp, h } from "vue";
import { RouterView } from "vue-router";

import { router } from "./router";

function bootstrap(): void {
	createApp({
		name: "AppRoot",
		render: () => h(RouterView),
	})
		.use(router)
		.mount("#app");
}

bootstrap();
