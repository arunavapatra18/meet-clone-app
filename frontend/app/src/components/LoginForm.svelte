<script lang="ts">
	import { redirect } from "@sveltejs/kit";

    let username = ''
    let password = ''

    let login_user = async () => {
      const endpoint = 'http://localhost:8000/auth/login/'
      const requestOpts = {
        method: "POST",
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: new URLSearchParams({username, password}),
        credentials: 'include' as RequestCredentials,
      }
      try {
        const response = await fetch(endpoint, requestOpts)
      
        if (response.ok) {
          window.location.href = "/home"
        }
        else {
          const errorData = await response.json()
          console.error('Login failed: ', errorData)
        }
      } catch (error) {
        console.error('An error occured: ', error)
      }
    }
</script>

<div class="hero bg-base-200 min-h-screen">
    <div class="hero-content flex-col lg:flex-row-reverse">
      <div class="text-center lg:text-left">
        <h1 class="text-5xl font-bold">Glad to See You Again!</h1>
        <p class="py-6">
            Enter your details to dive back into seamless communication with those who matter most.
        </p>
      </div>
      <div class="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl">
        <form class="card-body" on:submit|preventDefault={login_user}>
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
            <button class="btn btn-primary">Login</button>
          </div>
        </form>
        <div class="mb-2 mx-auto">
            <button class="btn btn-ghost" on:click={()=>window.location = '/register'}>Join now!</button>
        </div>
      </div>
    </div>
  </div>