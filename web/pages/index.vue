<template>
  <div class="bg-gradient-to-t from-slate-800 via-slate-900 to-slate-950 p-5 bg-full">
    <div
        class="text-center font-mono font-light italic py-10">
      <!-- change to css property -->
      <p id="title"
         class="md:text-6xl bg-gradient-to-r from-slate-300 via-blue-250 to-blue-500 inline-block text-transparent bg-clip-text">
        HAVE I BEEN FANED</p>
    </div>

    <UsernameForm class="flex flex-col items-center"/>
    <DatabaseStatus class="flex flex-col items-center"/>
    <HowTo class="flex flex-col items-center"/>
    <UpcomingFeatures class="flex flex-col items-center"/>
  </div>
</template>
