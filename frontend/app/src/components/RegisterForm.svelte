<script lang="ts">
	import { goto } from "$app/navigation";

    let username = ''
    let password = ''

    let register_user = async () => {
      const endpoint = 'http://localhost:8000/auth/register/'
      const requestOpts = {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email: username, password: password})
      }
      try {
        const response = await fetch(endpoint, requestOpts)
      
        if (response.ok) {
          goto('/login')
        }
        else {
          const errorData = await response.json()
          console.error('Registration failed: ', errorData)
        }
      } catch (error) {
        console.error('An error occured: ', error)
      }
    }
</script>

<div class="hero bg-base-200 min-h-screen">
    <div class="hero-content flex-col lg:flex-row-reverse">
      <div class="text-center lg:text-left">
        <h1 class="text-5xl font-bold">Join now!</h1>
        <p class="py-6">
            Create your account in seconds and connect with friends, family, and colleagues from anywhere. It’s fast, secure, and free to get started!
        </p>
      </div>
      <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
        <form class="card-body" on:submit|preventDefault={register_user}>
          <div class="form-control">
            <label class="label">
              <span class="label-text">Email</span>
            </label>
            <input type="email" placeholder="email" class="input input-bordered" bind:value={username} required />
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text">Password</span>
            </label>
            <input type="password" placeholder="password" class="input input-bordered" bind:value={password} required />
            <label class="label">
              <a href="#" class="label-text-alt link link-hover">Forgot password?</a>
            </label>
          </div>
          <div class="form-control mt-6">
            <button class="btn btn-primary">Join</button>
          </div>
        </form>
        <div class="mb-2 mx-auto">
            <button class="btn btn-ghost" on:click={()=>window.location = '/login'}>Login</button>
        </div>
      </div>
    </div>
  </div>
