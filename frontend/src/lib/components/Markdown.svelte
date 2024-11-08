<script lang="ts">
  import 'github-markdown-css/github-markdown-light.css';
  import markdownit from 'markdown-it';

  let { body = $bindable() }: { body: string } = $props();

  const md = markdownit();
  const bodyHtml = $derived(md.render(body));
</script>

<article class="markdown-body">
  {@html bodyHtml}
</article>

<style>
  :global(
      .markdown-body h1,
      .markdown-body h2,
      .markdown-body h3,
      .markdown-body h4,
      .markdown-body h5,
      .markdown-body h6
    ) {
    border-bottom: none;
  }
</style>
