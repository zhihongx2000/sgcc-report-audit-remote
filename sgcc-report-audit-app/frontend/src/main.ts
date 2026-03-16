import { createApp } from "vue";

import "./assets/styles/variables.css";
import "./assets/styles/global.css";
import App from "./App.vue";
import { router } from "./router";

function bootstrap(): void {
	createApp(App).use(router).mount("#app");
}

bootstrap();
