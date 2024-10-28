<div class="hero bg-base-200 min-h-screen">
    <div class="hero-content flex-col lg:flex-row">
      <img
        src="video-call.svg"
        class="max-w-xl rounded-lg" 
        alt="video-call-clipart"/>
      <div>
        <h1 class="text-4xl font-bold">Your Conversations, Your Way</h1>
        <p class="py-6">
            From simple text messages to high-quality video calls, we’re here to make connecting easy and enjoyable. Say hello to seamless communication at your fingertips.
        </p>
        <div class="flex gap-x-3 lg:gap-x-6">
            <button class="btn btn-primary" on:click={()=>window.location = '/login'}>Start Connecting</button>
            <form class="relative w-60">
                <input type="text" placeholder="Meeting ID" class="input input-bordered w-full max-w-xs" />
                <button class="absolute top-1/4 right-4" type="submit">Join</button>
            </form>
        </div>
      </div>
    </div>
  </div>