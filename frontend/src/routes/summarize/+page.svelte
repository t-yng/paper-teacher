<script lang="ts">
	import Markdown from '$lib/components/Markdown.svelte';
	import { Select, A } from 'flowbite-svelte';
	import { ArrowLeftOutline } from 'flowbite-svelte-icons';
	import { paperStore, type Paper } from '$lib/stores/paper';
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
	let selectedSection = $state(sections.length > 0 ? sections[0] : null);
	let markdownBody = $state(makeContent(selectedSection));

	const selectSection = (value: string) => {
		const section = sections.find((section) => section.heading === value) ?? null;
		selectedSection = section;
		markdownBody = makeContent(selectedSection);
	};
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
				<Markdown bind:body={markdownBody} />
			</div>
			<div class="border border-solid border-black p-4"></div>
		</div>
	</div>
</main>
