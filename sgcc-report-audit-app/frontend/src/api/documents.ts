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

export type BrowserImageReference = {
	id: string;
	caption: string;
	source: string;
	page: number | null;
	highlight: string;
};

export type BrowserChunkMetadata = {
	title: string;
	summary: string;
	tags: string[];
	headingPath: string;
	source: string;
	page: number | null;
	docType: "pdf" | "docx";
	ingestedAt: string;
	imageRefs: BrowserImageReference[];
};

export type BrowserChunkRecord = {
	chunkId: string;
	chunkIndex: number;
	text: string;
	metadata: BrowserChunkMetadata;
};

export type BrowserDocumentSummary = {
	documentId: string;
	reportName: string;
	sourcePath: string;
	collection: string;
	chunkCount: number;
	imageCount: number;
	ingestedAt: string;
};

export type BrowserDocumentDetail = {
	summary: BrowserDocumentSummary;
	chunks: BrowserChunkRecord[];
};

export type ListBrowserDocumentsOptions = {
	collection?: string;
	query?: string;
};

export type IngestionTaskStatus = "queued" | "running" | "failed" | "done";

export type IngestionTaskRecord = {
	taskId: string;
	sourcePath: string;
	collection: string;
	status: IngestionTaskStatus;
	progressPercent: number;
	startedAt: string;
	updatedAt: string;
	errorMessage: string | null;
	retryCount: number;
	inputMode: "path" | "upload";
};

export type StartIngestionInput = {
	sourcePath?: string;
	fileName?: string;
	collection?: string;
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
					paragraphAnchor: `sec-${checkNumber}-p1`,
					imageHint: null,
					excerpt: `第 ${checkNumber} 项正文证据，包含判定条件、约束边界与引用依据。`,
				},
				{
					id: `${checkId}-e2-${reportId}`,
					label: "附录截图",
					source: `appendix-${String((checkNumber % 5) + 1).padStart(2, "0")}`,
					page: checkNumber + 9,
					paragraphAnchor: `fig-${checkNumber}-a`,
					imageHint: `图 ${String((checkNumber % 5) + 1).padStart(2, "0")} 波形截图`,
					excerpt: "截图中标注了谐波与电压波动关键读数，可作为图像证据定位。",
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

type BrowserSeed = {
	summary: Omit<BrowserDocumentSummary, "chunkCount" | "imageCount">;
	chunks: Omit<BrowserChunkRecord, "chunkIndex">[];
};

const BROWSER_SEEDS: BrowserSeed[] = [
	{
		summary: {
			documentId: "doc-20260317-grid-harmonic",
			reportName: "华东区域风光储并网电能质量评估报告",
			sourcePath: "data/documents/sgcc-default/华东区域风光储并网电能质量评估报告.docx",
			collection: "sgcc-default",
			ingestedAt: "2026-03-17T17:26:12.000Z",
		},
		chunks: [
			{
				chunkId: "doc1-c001",
				text: "报告章节指出 220kV 接入点在高风速工况下存在 5 次谐波放大，推荐结合 SVG 与分组滤波器开展治理。",
				metadata: {
					title: "接入点谐波风险识别",
					summary: "描述高风速并网工况下谐波波动区间与风险等级。",
					tags: ["谐波", "接入点", "风险分级"],
					headingPath: "3.2/3.2.4",
					source: "chapter-3.2",
					page: 17,
					docType: "docx",
					ingestedAt: "2026-03-17T17:26:12.000Z",
					imageRefs: [
						{
							id: "doc1-c001-img1",
							caption: "图 3-4 谐波放大区间趋势",
							source: "appendix-03",
							page: 18,
							highlight: "18:20-18:35 区间峰值明显上冲",
						},
					],
				},
			},
			{
				chunkId: "doc1-c002",
				text: "仿真与实测对比中，背景电压畸变率在 1.8%~2.1%，当并网容量提升至 92% 时接近约束上限，建议执行动态补偿策略。",
				metadata: {
					title: "背景与计算叠加分析",
					summary: "对比背景值与并网后预测值，识别临界区间。",
					tags: ["背景值", "叠加", "临界区间"],
					headingPath: "4.1/4.1.2",
					source: "chapter-4.1",
					page: 22,
					docType: "docx",
					ingestedAt: "2026-03-17T17:26:12.000Z",
					imageRefs: [],
				},
			},
			{
				chunkId: "doc1-c003",
				text: "结论章节建议在 35kV 侧增加在线监测点，监测周期不少于 14 天，并与现有调度日志建立关联。",
				metadata: {
					title: "治理与监测建议",
					summary: "提出治理设备与监测周期建议，明确实施窗口。",
					tags: ["治理建议", "在线监测", "调度日志"],
					headingPath: "6.3",
					source: "chapter-6.3",
					page: 31,
					docType: "docx",
					ingestedAt: "2026-03-17T17:26:12.000Z",
					imageRefs: [
						{
							id: "doc1-c003-img1",
							caption: "图 6-2 在线监测点位布局",
							source: "chapter-6.3",
							page: 32,
							highlight: "监测点覆盖 PCC 与关键支路",
						},
					],
				},
			},
		],
	},
	{
		summary: {
			documentId: "doc-20260317-coastal-wind",
			reportName: "沿海风电接入系统电能质量复核报告",
			sourcePath: "data/documents/sgcc-default/沿海风电接入系统电能质量复核报告.pdf",
			collection: "sgcc-default",
			ingestedAt: "2026-03-17T17:08:24.000Z",
		},
		chunks: [
			{
				chunkId: "doc2-c001",
				text: "复核报告确认并网方案与审批路径完整，但部分图纸版本号不一致，需要补充最新版附录。",
				metadata: {
					title: "审批链路一致性复核",
					summary: "核验审批文件链路，并标记图纸版本偏差。",
					tags: ["审批", "版本管理", "附录"],
					headingPath: "2.1/2.1.3",
					source: "chapter-2.1",
					page: 9,
					docType: "pdf",
					ingestedAt: "2026-03-17T17:08:24.000Z",
					imageRefs: [],
				},
			},
			{
				chunkId: "doc2-c002",
				text: "潮汐工况下，谐波电流峰值与母线负载存在相位错位，建议在高负荷时段执行分段限值监控。",
				metadata: {
					title: "潮汐工况谐波波动",
					summary: "识别潮汐工况导致的波动与负荷错位关系。",
					tags: ["潮汐工况", "谐波电流", "限值监控"],
					headingPath: "3.4",
					source: "chapter-3.4",
					page: 14,
					docType: "pdf",
					ingestedAt: "2026-03-17T17:08:24.000Z",
					imageRefs: [
						{
							id: "doc2-c002-img1",
							caption: "图 3-2 潮汐负荷与谐波峰值对齐图",
							source: "chapter-3.4",
							page: 15,
							highlight: "高负荷段出现双峰重叠",
						},
					],
				},
			},
		],
	},
	{
		summary: {
			documentId: "doc-20260316-rail-harmonic",
			reportName: "城轨供电系统谐波评估专项报告",
			sourcePath: "data/documents/sgcc-archive/城轨供电系统谐波评估专项报告.pdf",
			collection: "sgcc-archive",
			ingestedAt: "2026-03-16T20:21:03.000Z",
		},
		chunks: [
			{
				chunkId: "doc3-c001",
				text: "报告显示牵引负载突变会引起短时电压波动，建议在站间区段配置快速调节装置。",
				metadata: {
					title: "牵引负载突变影响",
					summary: "分析牵引场景下电压波动触发条件。",
					tags: ["牵引负载", "电压波动", "快速调节"],
					headingPath: "5.2",
					source: "chapter-5.2",
					page: 27,
					docType: "pdf",
					ingestedAt: "2026-03-16T20:21:03.000Z",
					imageRefs: [
						{
							id: "doc3-c001-img1",
							caption: "图 5-5 牵引波动与恢复曲线",
							source: "chapter-5.2",
							page: 28,
							highlight: "负载突变后 1.2s 内恢复至阈值区间",
						},
					],
				},
			},
		],
	},
];

const BROWSER_DETAILS: Record<string, BrowserDocumentDetail> = Object.fromEntries(
	BROWSER_SEEDS.map((seed) => {
		const chunks = seed.chunks.map((chunk, index) => ({
			...chunk,
			chunkIndex: index + 1,
		}));

		const imageCount = chunks.reduce(
			(total, item) => total + item.metadata.imageRefs.length,
			0,
		);

		const detail: BrowserDocumentDetail = {
			summary: {
				...seed.summary,
				chunkCount: chunks.length,
				imageCount,
			},
			chunks,
		};

		return [seed.summary.documentId, detail];
	}),
);

const DEFAULT_INGESTION_COLLECTION = "sgcc-default";
const INGESTION_FAILURE_HINT =
	"摄取阶段 split 失败：文档结构异常，请检查文件编码或重试。";

const INGESTION_SEEDS: IngestionTaskRecord[] = [
	{
		taskId: "ing-task-legacy-failed",
		sourcePath:
			"/data/documents/sgcc-default/legacy-fail-sample.docx",
		collection: "sgcc-default",
		status: "failed",
		progressPercent: 64,
		startedAt: "2026-03-17T18:22:10.000Z",
		updatedAt: "2026-03-17T18:24:48.000Z",
		errorMessage: INGESTION_FAILURE_HINT,
		retryCount: 0,
		inputMode: "path",
	},
	{
		taskId: "ing-task-running-001",
		sourcePath: "/data/documents/sgcc-default/coastal-grid-2026.pdf",
		collection: "sgcc-default",
		status: "running",
		progressPercent: 42,
		startedAt: "2026-03-17T18:31:12.000Z",
		updatedAt: "2026-03-17T18:32:03.000Z",
		errorMessage: null,
		retryCount: 0,
		inputMode: "upload",
	},
	{
		taskId: "ing-task-done-001",
		sourcePath: "/data/documents/sgcc-archive/harmonic-audit-2025.pdf",
		collection: "sgcc-archive",
		status: "done",
		progressPercent: 100,
		startedAt: "2026-03-17T17:02:08.000Z",
		updatedAt: "2026-03-17T17:03:15.000Z",
		errorMessage: null,
		retryCount: 0,
		inputMode: "path",
	},
];

let ingestionSequence = 2;
let ingestionTasks: IngestionTaskRecord[] = cloneIngestionTasks(INGESTION_SEEDS);

function cloneItems(items: readonly AuditCheckItem[]): AuditCheckItem[] {
	return items.map((item) => ({
		...item,
		evidence: item.evidence.map((entry) => ({ ...entry })),
	}));
}

function cloneBrowserImageRefs(
	items: readonly BrowserImageReference[],
): BrowserImageReference[] {
	return items.map((item) => ({ ...item }));
}

function cloneBrowserChunks(
	items: readonly BrowserChunkRecord[],
): BrowserChunkRecord[] {
	return items.map((item) => ({
		...item,
		metadata: {
			...item.metadata,
			tags: [...item.metadata.tags],
			imageRefs: cloneBrowserImageRefs(item.metadata.imageRefs),
		},
	}));
}

function cloneIngestionTasks(
	items: readonly IngestionTaskRecord[],
): IngestionTaskRecord[] {
	return items.map((item) => ({ ...item }));
}

function resolveSourcePath(payload: StartIngestionInput): {
	sourcePath: string;
	inputMode: "path" | "upload";
	collection: string;
} {
	const collection = payload.collection?.trim() || DEFAULT_INGESTION_COLLECTION;
	const sourcePath = payload.sourcePath?.trim();
	if (sourcePath) {
		return {
			sourcePath,
			inputMode: "path",
			collection,
		};
	}

	const fileName = payload.fileName?.trim();
	if (fileName) {
		return {
			sourcePath: `/data/documents/${collection}/${fileName}`,
			inputMode: "upload",
			collection,
		};
	}

	throw new Error("sourcePath or fileName is required");
}

function advanceTaskProgress(task: IngestionTaskRecord, nowIso: string): IngestionTaskRecord {
	if (task.status === "done" || task.status === "failed") {
		return task;
	}

	const next: IngestionTaskRecord = { ...task };
	next.updatedAt = nowIso;

	if (next.status === "queued") {
		next.status = "running";
		next.progressPercent = Math.max(8, next.progressPercent);
		return next;
	}

	const shouldFailThisRun =
		next.retryCount === 0 && next.sourcePath.toLowerCase().includes("fail");
	const increment = Math.max(10, 18 - next.retryCount * 3);
	const progressed = Math.min(100, next.progressPercent + increment);

	if (shouldFailThisRun && progressed >= 70) {
		next.status = "failed";
		next.progressPercent = progressed;
		next.errorMessage = INGESTION_FAILURE_HINT;
		return next;
	}

	next.progressPercent = progressed;
	next.errorMessage = null;
	if (progressed >= 100) {
		next.status = "done";
	}

	return next;
}

function tickIngestionTasks(): void {
	const nowIso = new Date().toISOString();
	ingestionTasks = ingestionTasks.map((task) => advanceTaskProgress(task, nowIso));
}

export function resetIngestionTaskState(): void {
	ingestionSequence = 2;
	ingestionTasks = cloneIngestionTasks(INGESTION_SEEDS);
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

export async function listBrowserDocuments(
	options: ListBrowserDocumentsOptions = {},
): Promise<BrowserDocumentSummary[]> {
	const collectionFilter = options.collection?.trim().toLowerCase();
	const queryFilter = options.query?.trim().toLowerCase();

	return Object.values(BROWSER_DETAILS)
		.map((detail) => ({ ...detail.summary }))
		.filter((item) => {
			if (
				collectionFilter &&
				collectionFilter !== "all" &&
				item.collection.toLowerCase() !== collectionFilter
			) {
				return false;
			}

			if (!queryFilter) {
				return true;
			}

			const searchable = `${item.reportName} ${item.sourcePath} ${item.documentId}`.toLowerCase();
			return searchable.includes(queryFilter);
		})
		.sort((left, right) => Date.parse(right.ingestedAt) - Date.parse(left.ingestedAt));
}

export async function getBrowserDocumentDetail(
	documentId: string,
): Promise<BrowserDocumentDetail> {
	const detail = BROWSER_DETAILS[documentId];
	if (!detail) {
		throw new Error(`Unknown document: ${documentId}`);
	}

	return {
		summary: { ...detail.summary },
		chunks: cloneBrowserChunks(detail.chunks),
	};
}

export async function listIngestionTasks(): Promise<IngestionTaskRecord[]> {
	tickIngestionTasks();
	return cloneIngestionTasks(ingestionTasks).sort(
		(left, right) => Date.parse(right.startedAt) - Date.parse(left.startedAt),
	);
}

export async function startIngestion(
	payload: StartIngestionInput,
): Promise<IngestionTaskRecord> {
	const normalized = resolveSourcePath(payload);
	ingestionSequence += 1;

	const nowIso = new Date().toISOString();
	const task: IngestionTaskRecord = {
		taskId: `ing-task-${String(ingestionSequence).padStart(3, "0")}`,
		sourcePath: normalized.sourcePath,
		collection: normalized.collection,
		status: "queued",
		progressPercent: 0,
		startedAt: nowIso,
		updatedAt: nowIso,
		errorMessage: null,
		retryCount: 0,
		inputMode: normalized.inputMode,
	};

	ingestionTasks = [task, ...ingestionTasks];
	return { ...task };
}

export async function retryTask(taskId: string): Promise<IngestionTaskRecord> {
	const normalizedTaskId = taskId.trim();
	const index = ingestionTasks.findIndex((item) => item.taskId === normalizedTaskId);
	if (index < 0) {
		throw new Error(`Unknown task: ${taskId}`);
	}

	const current = ingestionTasks[index];
	if (current.status !== "failed") {
		throw new Error(`Task is not failed: ${taskId}`);
	}

	const nowIso = new Date().toISOString();
	const retried: IngestionTaskRecord = {
		...current,
		status: "running",
		progressPercent: Math.max(18, current.progressPercent - 26),
		updatedAt: nowIso,
		errorMessage: null,
		retryCount: current.retryCount + 1,
	};

	ingestionTasks = [
		...ingestionTasks.slice(0, index),
		retried,
		...ingestionTasks.slice(index + 1),
	];

	return { ...retried };
}
