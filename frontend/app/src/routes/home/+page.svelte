<script lang="ts">
    let meeting_id = ''
</script>

<div>
    <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl content-center">
        <form class="card-body">
            <div class="form-control">
                <input type="email" id="meeting-id" placeholder="Room Name" class="input input-bordered" bind:value={meeting_id} required />
            </div>
            <div class="form-control mt-6">
                <button class="btn btn-primary">Join</button>
            </div>
        </form>
    </div>
</div>