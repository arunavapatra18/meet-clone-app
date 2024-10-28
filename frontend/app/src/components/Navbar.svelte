<script>
	import AuthButton from "./AuthButton.svelte";
	import ProfileBadge from "./ProfileBadge.svelte";
	let { landing = true } = $props()
</script>

<div class="navbar lg:sticky lg:top-0">
	<div class="flex-1">
	  <a href="/" class="btn btn-ghost text-xl">connectNow</a>
	</div>
	{#if landing}
    	<AuthButton />
	{:else}
		<ProfileBadge />
	{/if}
</div>