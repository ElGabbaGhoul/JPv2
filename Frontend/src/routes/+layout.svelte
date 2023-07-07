<script>
	import '../app.postcss';
	import NavMenu from '$lib/components/NavMenu.svelte';
	import { isLoggedIn } from '$lib/stores/stores';
</script>

<div class="app">
	<main>
		{#if $isLoggedIn}
			<NavMenu />
		{/if}
		<slot />
	</main>

	<div />
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
		padding: 1rem;
		width: 100%;
		max-width: 64rem;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>
