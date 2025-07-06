<template>
  <div class="bg-gradient-to-t from-slate-800 via-slate-900 to-slate-950 flex flex-col items-center p-5 h-full">
    <div
        class="text-center font-mono font-light italic py-10">
      <!-- change to css property -->
      <p id="title"
          class="sd:text-lg md:text-6xl bg-gradient-to-r from-slate-300 via-blue-250 to-blue-500 inline-block text-transparent bg-clip-text">
        HAVE I BEEN FANED</p>
    </div>

    <UsernameForm/>
    <DatabaseStatus/>
    <UpcomingFeatures/>
  </div>
</template>
