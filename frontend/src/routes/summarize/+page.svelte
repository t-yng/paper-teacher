<script lang="ts">
	import { Select, A } from 'flowbite-svelte';
	import { ArrowLeftOutline } from 'flowbite-svelte-icons';

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
</script>

<main class="h-[100%] pb-8 pt-24">
	<div class="w-max-[1200px] flex h-[100%] w-screen flex-col px-8">
		<A href="/"><ArrowLeftOutline class="me-2 h-6 w-6" /> Back</A>
		<div class="mb-4 w-full">
			<Select items={sections} value="abstract" size="sm" class="w-[150px]" />
		</div>
		<div class="grid flex-1 grid-cols-2 gap-8">
			<div class="border border-solid border-black p-4"></div>
			<div class="border border-solid border-black p-4"></div>
		</div>
	</div>
</main>
