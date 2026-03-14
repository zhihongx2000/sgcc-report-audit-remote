const APP_HTML = `
	<main style="font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif; padding: 24px; line-height: 1.6;">
		<h1 style="margin: 0 0 12px;">SGCC Report Audit</h1>
		<p style="margin: 0; color: #374151;">
			Frontend bootstrap entry is ready. Full Vue page wiring will be completed in upcoming tasks.
		</p>
	</main>
`;

export function bootstrap(): void {
	const root = document.getElementById("app");
	if (!root) {
		console.error("[frontend] #app root container is missing");
		return;
	}

	root.innerHTML = APP_HTML;
}

if (document.readyState === "loading") {
	document.addEventListener("DOMContentLoaded", bootstrap, { once: true });
} else {
	bootstrap();
}
