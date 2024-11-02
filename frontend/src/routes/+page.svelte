<script lang="ts">
	import { goto } from '$app/navigation';
	import FileInput from '$lib/components/FileInput.svelte';
	import { Select, Label, GradientButton, Spinner } from 'flowbite-svelte';
	import { paperStore } from '$lib/stores/paper';

	let selectedLanguage = 'japanese';
	let summarizing = false;
	const languages = [
		{
			value: 'japanese',
			name: 'Japanese'
		},
		{
			value: 'english',
			name: 'English'
		}
	];

	const requestSummarize = async (file: File) => {
		summarizing = true;
		const formData = new FormData();
		formData.append('file', file);

		try {
			const response = await fetch('http://localhost:8000/papers/extract', {
				method: 'POST',
				body: formData
			});
			const data = await response.json();
			return data;
		} catch (error) {
			console.error('Failed extract data from pdf', error);
			throw error;
		} finally {
			summarizing = false;
		}
	};

	const handleSubmit = async (event: SubmitEvent) => {
		event.preventDefault();
		const form = event.target as HTMLFormElement;
		// TODO: アップロードされたPDFを取得
		const formData = new FormData(form);
		const file = formData.get('paper') as File;

		try {
			const paper = await requestSummarize(file);
			paperStore.set(paper);
			goto('/summarize');
		} catch (error) {
			console.error('Failed to summarize', error);
			alert('Failed to summarize. Please try again after.');
			return;
		}
	};
</script>

<main class="flex h-full flex-col items-center justify-center">
	<form
		class="flex max-w-[800px] flex-col items-center justify-center gap-4"
		on:submit={handleSubmit}
	>
		<!-- Upload paper -->
		<div class="w-[500px]">
			<FileInput name="paper" />
		</div>
		<div class="self-start">
			<Label for="output-language" class="mb-2">Output Language</Label>
			<Select items={languages} value={selectedLanguage} size="sm" class="w-[150px]" />
		</div>
		<GradientButton type="submit" color="purpleToBlue" class="mx-auto block">
			{#if summarizing}
				<Spinner class="me-3" size="4" color="white" />Uploading ...
			{:else}Summarize{/if}
		</GradientButton>
	</form>
</main>
