<script>
// import axios from "axios";
// import { parse as jsrootParse } from 'jsroot';
import { store } from '../stores/RootHistogramStore';

export default {
  name: 'Hists',
  data() {
    return {
      hists: store.hists,
      confDir: store.confDir,
    };
  },
  methods: {
    async getDirs() {
      store.hists = await axios.post("/get-json-file", { params: { q: this.confDir.mainPath } });
    }
  },
};

console.log(store.confDir);

</script>
<template>
  <form @submit.prevent="getDirs">
    <label for=" search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
    <div class="relative">
      <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
          fill="none" viewBox="0 0 20 20">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
        </svg>
      </div>
      <input v-model="store.confDir" type="search" id="search"
        class="block w-full p-4 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Search" required>
      <button type="button" @click="store.getHistogramDirs(rootDir)"
        class="text-white absolute right-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
        Search
      </button>

    </div>
  </form>

  <!-- <p>Message is: {{ histograms }}</p> -->
  <!-- <div id="main" class="flex flex-col items-center justify-center w-full mt-2 mb-12">
    <div class="ml-12 mr-12 grid grid-cols-3 gap-x-20 gap-y-5">
      <div class="" v-for="( item, index ) in histograms">
        {{ index }}
        <div class="w-96 h-96 flex" v-bind:id="item.id">
          {{ drawHistJson(item.hist, item.id) }}
        </div>
      </div>
    </div>
  </div> -->
</template>
