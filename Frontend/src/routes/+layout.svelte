<script>
	import '../app.postcss';
	import NavMenu from '$lib/components/NavMenu.svelte';
	import { isLoggedIn } from '$lib/stores/stores';
</script>

<div class="app">
	<main>
		{#if $isLoggedIn}
			<NavMenu />
			<hr class="my-4" />
		{/if}
		<slot />
	</main>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
		background-color: grey;
	}

	main {
		flex: 1;
		display: flex;
		flex-direction: column;
		width: 100%;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>
