<!-- <script lang="ts">
    import { checkAuth } from "$lib/auth";
    import { redirect } from "@sveltejs/kit";
	import { onMount } from "svelte";

    onMount(async () => {
        const isAuthenticated = await checkAuth();
        if (!isAuthenticated) {
            throw redirect(302, "/login");
        }
    })
</script> -->
<div>
    Hello, world!
</div>