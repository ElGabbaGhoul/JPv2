<script>
	import HomeIcon from '$lib/components/Icons/HomeIcon.svelte';
	import SearchIcon from '$lib/components/Icons/SearchIcon.svelte';
	import LibraryIcon from '$lib/components/Icons/LibraryIcon.svelte';
	import AccountIcon from '$lib/components/Icons/AccountIcon.svelte';
	import LogoutIcon from '$lib/components/Icons/LogoutIcon.svelte';
	import { isLoggedIn } from '$lib/stores/stores';
</script>

<nav class="bg-slate-700">
	<ul class="flex flex-row gap-5 text-white">
		<li><a class="flex flex-row gap-2 items-center" href="/home"><HomeIcon />Home</a></li>
		<li><a class="flex flex-row gap-1.5 items-center" href="/search"><SearchIcon />Search</a></li>
		<li><a class="flex flex-row gap-2 items-center" href="/library"><LibraryIcon />Library</a></li>
		<li>
			<a class="flex flex-row gap-1 items-center" href="/account"><AccountIcon />Account</a>
		</li>
		<li class="flex flex-grow justify-end">
			<a
				class="flex flex-row gap-1 items-center"
				href="/"
				on:click={() => {
					$isLoggedIn = false;
				}}><LogoutIcon />Logout</a
			>
		</li>
	</ul>
</nav>
