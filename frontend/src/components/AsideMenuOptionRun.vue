<script setup>
import { usePlotsStore } from "@/stores/plots.js";
import { storeToRefs } from "pinia";
import { watch, ref } from 'vue';

defineProps({
  items: {
    type: Object,
    default: {}
  },
});
const show = ref(true);
const plotsStore = usePlotsStore();

/* Make store variable reflective */
const { inputSelectedRuns } = storeToRefs(plotsStore)

watch(inputSelectedRuns, (val) => {
  // console.log(`[DEBUG] selected runs change: ${inputSelectedRuns.value}`)
  plotsStore.updateHistograms()
})

function toggleDropdown() { show.value = !show.value }
</script>

<template>
  <div>
    <div>
      <button id="dropdownRuns" data-dropdown-toggle="dropdownBgHover" @click="toggleDropdown"
        class="justify-center items-center text-center font-normal rounded w-full text-sm px-2 py-1 inline-flex focus:ring text-white bg-blue-700 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800  hover:bg-blue-800 focus:outline-none focus:ring-blue-300"
        type="button">
        Select Runs
        <svg class="w-2.5 h-2.5 ml-2.5" aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
          <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"
            d="m1 1 4 4 4-4" />
        </svg>
      </button>
    </div>
    <div class="z-auto bg-white items-center rounded-sm dark:bg-gray-700" v-if="show">
      <ul class="p-1 text-xs text-gray-700 dark:text-gray-200" aria-labelledby="dropdownBgHoverButton">

        <!-- 
          - Given "ptops.items" is  "availableRunEraDict" which is Object with {run:era} structure. 
          - In Vue, iterate convention for dictionary kind object is (value, key, index), here value is era and key is run which is bind to ":value" and updates v-model="inputSelectedRuns"
          - Keep in mind that "inputSelectedRuns" is initialized with availableRunEraDict.keys() .
        -->
        <li v-for="(value_era, key_run, index) in items" :key="'run_checkbox_' + index">
          <div class="flex p-1 items-end rounded hover:bg-gray-100 dark:hover:bg-gray-600">
            <input type="checkbox" :id="'run_checkbox_' + index" :value="key_run" v-model="inputSelectedRuns"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-1 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 dark:bg-gray-600 dark:border-gray-500">
            <label :for="'run_checkbox_' + index"
              class="w-full px-1 text-xs font-medium text-gray-900 rounded dark:text-gray-300">
              {{ key_run }} : {{ value_era }}
            </label>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
