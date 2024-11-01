<script lang="ts">
	import { goto } from '$app/navigation';
	import FileInput from '$lib/components/FileInput.svelte';
	import { Select, Label, GradientButton, Spinner } from 'flowbite-svelte';

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

	const requestSummarize = () => {
		summarizing = true;
		// TODO: PDFからサマリを生成するAPIリクエストを送信
		return new Promise<void>((resolve, reject) => {
			setTimeout(() => {
				resolve();
			}, 2000);
		});
	};

	const handleSubmit = async (event: SubmitEvent) => {
		event.preventDefault();
		const form = event.target as HTMLFormElement;
		// TODO: アップロードされたPDFを取得
		const formData = new FormData(form);

		await requestSummarize();
		goto('/summarize');
	};
</script>

<main class="flex h-full flex-col items-center justify-center">
	<form
		class="flex max-w-[800px] flex-col items-center justify-center gap-4"
		on:submit={handleSubmit}
	>
		<!-- Upload paper -->
		<div class="w-[500px]">
			<FileInput />
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
