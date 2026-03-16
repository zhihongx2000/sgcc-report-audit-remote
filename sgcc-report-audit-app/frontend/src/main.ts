import { createApp } from "vue";

import App from "./App.vue";
import { router } from "./router";

function bootstrap(): void {
	createApp(App).use(router).mount("#app");
}

bootstrap();
