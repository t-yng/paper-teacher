<script lang="ts">
	import Markdown from '$lib/components/Markdown.svelte';
	import { Select, A } from 'flowbite-svelte';
	import { ArrowLeftOutline } from 'flowbite-svelte-icons';
	import markdownit from 'markdown-it';

	const sections = [
		{
			value: 'abstract',
			name: 'Abstract'
		},
		{
			value: 'introduction',
			name: 'Introduction'
		}
	];

	const markdownBody = `# Hello, **world**!\n ## This is a test`;
</script>

<main class="h-[100%] pb-8 pt-24">
	<div class="w-max-[1200px] flex h-[100%] w-screen flex-col px-8">
		<A href="/"><ArrowLeftOutline class="me-2 h-6 w-6" /> Back</A>
		<div class="mb-4 w-full">
			<Select items={sections} value="abstract" size="sm" class="w-[150px]" />
		</div>
		<div class="grid flex-1 grid-cols-2 gap-8">
			<div class="border border-solid border-black p-4">
				<Markdown body={markdownBody} />
			</div>
			<div class="border border-solid border-black p-4"></div>
		</div>
	</div>
</main>
