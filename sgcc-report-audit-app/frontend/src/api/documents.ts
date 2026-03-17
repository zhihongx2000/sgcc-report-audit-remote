import type { AuditCheckItem, AuditCheckStatus } from "../stores/audit";

export type AuditReportStatus = "completed" | "running";

export type AuditReportSummary = {
	reportId: string;
	reportName: string;
	collection: string;
	status: AuditReportStatus;
	updatedAt: string;
	checkCount: number;
};

export type AuditReportDetail = {
	summary: AuditReportSummary;
	items: AuditCheckItem[];
};

const CHECK_TITLES = [
	"评估单位资质",
	"报告审批签章",
	"评估依据完整性",
	"用户接入信息",
	"用户设备参数",
	"用户干扰源特性",
	"原始提资资料",
	"电网设备信息",
	"电网容量信息",
	"评估指标覆盖",
	"指标限值选取",
	"背景测试数据",
	"背景与计算叠加",
	"仿真模型与截图",
	"评估考核点",
	"系统运行方式",
	"计算结果说明",
	"评估结论一致性",
	"治理建议有效性",
	"监测建议完整性",
];

const STATUS_REASON: Record<AuditCheckStatus, string> = {
	pass: "证据链完整，判定依据与报告结论一致。",
	review: "存在信息缺口，建议补充原始佐证后人工复核。",
	fail: "关键约束不满足，当前报告无法通过该项审查。",
};

type ReportSeed = {
	summary: Omit<AuditReportSummary, "checkCount">;
	statusPattern: AuditCheckStatus[];
};

function createItems(
	reportId: string,
	reportUpdatedAt: string,
	statusPattern: AuditCheckStatus[],
): AuditCheckItem[] {
	const baseTime = Date.parse(reportUpdatedAt);

	return CHECK_TITLES.map((title, index) => {
		const checkNumber = index + 1;
		const checkId = `check-${String(checkNumber).padStart(2, "0")}`;
		const status = statusPattern[index] ?? "review";

		return {
			id: checkId,
			title,
			status,
			reason: `${STATUS_REASON[status]}（${reportId} · 第 ${checkNumber} 项）`,
			evidence: [
				{
					id: `${checkId}-e1-${reportId}`,
					label: "正文段落",
					source: `chapter-${Math.ceil(checkNumber / 3)}.${(checkNumber % 3) + 1}`,
					page: checkNumber + 1,
				},
				{
					id: `${checkId}-e2-${reportId}`,
					label: "附录截图",
					source: `appendix-${String((checkNumber % 5) + 1).padStart(2, "0")}`,
					page: checkNumber + 9,
				},
			],
			updatedAt: new Date(baseTime - index * 60_000).toISOString(),
		};
	});
}

const REPORT_SEEDS: ReportSeed[] = [
	{
		summary: {
			reportId: "report-20260317-001",
			reportName: "华东区域风光储并网电能质量评估报告",
			collection: "sgcc-default",
			status: "completed",
			updatedAt: "2026-03-17T17:24:00.000Z",
		},
		statusPattern: [
			"pass",
			"pass",
			"review",
			"pass",
			"review",
			"pass",
			"fail",
			"pass",
			"review",
			"pass",
			"pass",
			"review",
			"fail",
			"review",
			"pass",
			"pass",
			"review",
			"pass",
			"fail",
			"review",
		],
	},
	{
		summary: {
			reportId: "report-20260317-002",
			reportName: "沿海风电接入系统电能质量复核报告",
			collection: "sgcc-default",
			status: "running",
				updatedAt: "2026-03-17T17:05:00.000Z",
		},
		statusPattern: [
			"review",
			"review",
			"pass",
			"pass",
			"review",
			"pass",
			"pass",
			"review",
			"pass",
			"pass",
			"pass",
			"review",
			"review",
			"pass",
			"pass",
			"review",
			"pass",
			"review",
			"fail",
			"review",
		],
	},
	{
		summary: {
			reportId: "report-20260316-007",
			reportName: "城轨供电系统谐波评估专项报告",
			collection: "sgcc-archive",
			status: "completed",
			updatedAt: "2026-03-16T20:18:00.000Z",
		},
		statusPattern: [
			"pass",
			"pass",
			"pass",
			"pass",
			"pass",
			"review",
			"pass",
			"pass",
			"review",
			"pass",
			"pass",
			"pass",
			"review",
			"pass",
			"pass",
			"pass",
			"pass",
			"pass",
			"review",
			"pass",
		],
	},
];

const REPORT_DETAILS: Record<string, AuditReportDetail> = Object.fromEntries(
	REPORT_SEEDS.map((seed) => {
		const items = createItems(
			seed.summary.reportId,
			seed.summary.updatedAt,
			seed.statusPattern,
		);

		const detail: AuditReportDetail = {
			summary: {
				...seed.summary,
				checkCount: items.length,
			},
			items,
		};

		return [seed.summary.reportId, detail];
	}),
);

function cloneItems(items: readonly AuditCheckItem[]): AuditCheckItem[] {
	return items.map((item) => ({
		...item,
		evidence: item.evidence.map((entry) => ({ ...entry })),
	}));
}

export async function listAuditReports(): Promise<AuditReportSummary[]> {
	return Object.values(REPORT_DETAILS)
		.map((detail) => ({ ...detail.summary }))
		.sort((left, right) => Date.parse(right.updatedAt) - Date.parse(left.updatedAt));
}

export async function getAuditReportDetail(
	reportId: string,
): Promise<AuditReportDetail> {
	const detail = REPORT_DETAILS[reportId];
	if (!detail) {
		throw new Error(`Unknown report: ${reportId}`);
	}

	return {
		summary: { ...detail.summary },
		items: cloneItems(detail.items),
	};
}
