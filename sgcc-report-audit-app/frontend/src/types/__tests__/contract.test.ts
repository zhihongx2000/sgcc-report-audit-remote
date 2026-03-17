import { readFileSync } from "node:fs";
import { resolve } from "node:path";

import { describe, expect, it } from "vitest";

import {
	BACKEND_CONTRACT_FIELD_SNAPSHOT,
	SGCC_BACKEND_CONTRACT_VERSION,
} from "../index";

function readDocSnapshot(): Record<string, string[]> {
	const docPath = resolve(process.cwd(), "../../docs/api/sgcc-backend-openapi.md");
	const markdown = readFileSync(docPath, "utf-8");
	const match = markdown.match(
		/<!-- CONTRACT_FIELD_SNAPSHOT_BEGIN -->[\s\S]*?```json\s*([\s\S]*?)\s*```[\s\S]*?<!-- CONTRACT_FIELD_SNAPSHOT_END -->/m,
	);

	if (!match) {
		throw new Error("contract snapshot block not found in sgcc-backend-openapi.md");
	}

	return JSON.parse(match[1]) as Record<string, string[]>;
}

describe("frontend-backend contract snapshot", () => {
	it("uses C10 frozen contract version", () => {
		expect(SGCC_BACKEND_CONTRACT_VERSION).toBe("2026-03-17.c10");
	});

	it("matches machine-readable snapshot in docs", () => {
		const docSnapshot = readDocSnapshot();
		expect(docSnapshot).toEqual(BACKEND_CONTRACT_FIELD_SNAPSHOT);
	});
});
