<script lang="ts">
	import Markdown from '$lib/components/Markdown.svelte';
	import { Select, A } from 'flowbite-svelte';
	import { ArrowLeftOutline } from 'flowbite-svelte-icons';
	import { paperStore, type Paper, type PaperSection } from '$lib/stores/paper';
	import { get } from 'svelte/store';

	const paper = get(paperStore);

	const sectionOptions = paper?.sections.map((section) => ({
		value: section.heading,
		name: section.heading
	}));

	const makeContent = (section: any) => {
		return `${'#'.repeat(section.level)} ${section.heading}\n${section.body}`;
	};

	const sections = paper?.sections ?? [];
	let selectedSection: PaperSection | null = $state(sections.length > 0 ? sections[0] : null);
	let sectionBodyMarkdown: string = $state('');
	let summaryMarkdown: string = $state('');
	let summaries: { [id: string]: string } = $state({});

	const getPreviousSummarizedSections = (sectionOrder: number) => {
		const summarizedSections = [];
		for (const [sectionId, summary] of Object.entries(summaries)) {
			const section = sections.find((section) => section.id === sectionId);
			if (section && section.order < sectionOrder) {
				summarizedSections.push(summary);
			}
		}

		return summarizedSections;
	};

	const fetchSummary = async (paper: Paper) => {
		if (selectedSection) {
			const response = await fetch(`http://localhost:8000/paper/sections/summarize`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					title: paper.title,
					language: 'japanese',
					section: sectionBodyMarkdown,
					summarized_sections: getPreviousSummarizedSections(selectedSection.order)
				})
			});
			const { summary } = await response.json();
			return summary;
		}
	};

	const selectSection = async (value: string) => {
		const section = sections.find((section) => section.heading === value) ?? null;
		selectedSection = section;
		sectionBodyMarkdown = makeContent(section);

		if (selectedSection == null || paper == null) {
			return;
		}

		if (summaries[selectedSection.id]) {
			summaryMarkdown = summaries[selectedSection.id];
		} else {
			const summary = await fetchSummary(paper);
			summaries[selectedSection.id] = summary;
			summaryMarkdown = summary;
		}
	};

	const initialize = async () => {
		if (paper && selectedSection) {
			sectionBodyMarkdown = makeContent(selectedSection);
			const summary = await fetchSummary(paper);
			summaries[selectedSection.id] = summary;
			summaryMarkdown = summary;
		}
	};

	initialize();
</script>

<main class="h-[100%] pb-8 pt-24">
	<div class="w-max-[1200px] flex h-[100%] w-screen flex-col px-8">
		<A href="/"><ArrowLeftOutline class="me-2 h-6 w-6" /> Back</A>
		<div class="mb-4 w-full">
			<Select
				items={sectionOptions}
				value={sectionOptions?.[0].value}
				size="sm"
				class="w-[150px]"
				onchange={(event) => {
					selectSection(event.currentTarget.value);
				}}
			/>
		</div>
		<div class="grid flex-1 grid-cols-2 gap-8">
			<div class="border border-solid border-black p-4">
				<Markdown bind:body={sectionBodyMarkdown} />
			</div>
			<div class="border border-solid border-black p-4">
				<Markdown bind:body={summaryMarkdown} />
			</div>
		</div>
	</div>
</main>
