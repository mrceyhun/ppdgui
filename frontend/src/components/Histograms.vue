<script setup>
import { computed, ref, watch } from 'vue';
import axios from 'axios';
import { drawHistJson } from '../utils/jsroot'

const errorMessage = ref('')
const input_run_year = ref(0)
const input_run_number = ref(0)

const user_input = reactive({
  run_year: 0,
  run_number: 0
});

const state = ref({
  run_number: 0,
  run_year: 0,
  detector_histograms: []
})

const hasHistogams = computed(() => {
  return state.detector_histograms.length > 0 ? true : false
})

const hasError = computed(() => {
  return errorMessage ? true : false
})

async function fetchRootData() {
  state.value = NaN
  try {
    errorMessage.value = null;
    const response = await axios.post("/v1/get-histogram-jsons",
      {
        "run_year": input_run_year.value,
        "run_number": input_run_number.value,
      });
    state.value = await response.data; // { run_number: 0, run_year: 0, detector_histograms: [] }

    // Set input placholder values to successful run year and number
    input_run_year.value = state.value.run_year
    input_run_number.value = state.value.run_number

    console.log("Response: " + input_run_year.value + ' - ' + input_run_number.value)
  } catch (error) {
    if (error.response) {
      console.log('Error', error.response.data.detail);
      errorMessage.value = error.response.data.detail;
      console.log(error.message);
    } else if (error.request) {
      console.log(error.request);
    } else {
      console.log('Error', error.message);
    }
  }
}
</script>

<template>
  <div class="px-8 pt-2 mx-auto lg:px-40 gap-2">
    <form @submit.prevent="fetchRootData" class="grid items-end gap-6 md:grid-cols-5">
      <div class="relative md:flex md:items-center mb-6"></div>
      <div class="relative md:flex md:items-center mb-6">
        <input v-model.lazy.number.trim="input_run_year" type="number" id="input_run_year"
          class="border border-gray-800 px-2.5 pb-0 pt-3 w-full text text-gray-900 rounded-sm focus:outline-none focus:ring-0 focus:border-blue-600 peer" />
        <label for="input_run_year"
          class="absolute text-xs text-gray-500 duration-300 transform -translate-y-2 scale-75 top-3 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1">
          Run year
        </label>
      </div>
      <div class="relative md:flex md:items-center mb-6">
        <input v-model.lazy.number.trim="input_run_number" type="number" id="input_run_number"
          class="border border-gray-800 px-2 pb-0 pt-3 w-full text text-gray-900 rounded-sm focus:outline-none focus:ring-0 focus:border-blue-600 peer" />
        <label for="input_run_number"
          class="absolute text-xs text-gray-500 duration-300 transform -translate-y-2 scale-75 top-3 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1">
          Run number
        </label>
      </div>
      <div class="relative md:flex md:items-center mb-6">
        <button
          class="shadow bg-purple-500 hover:bg-purple-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded">
          Show
        </button>
      </div>
      <div class="relative mb-6"></div>
    </form>
    <!-- ERROR MESSAGE -->

    <div v-if="hasError" class="p-4 mb-4 text-sm text-yellow-800 rounded-lg bg-yellow-50  " role="alert">
      <span class="font-medium">Warning alert!</span> {{ errorMessage }}
    </div>
    <!-- SHOW HISTOGRAMS -->
    <div v-if="hasHistogams" id="histograms">
      <main class="container px-8 pt-5 mx-auto grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="( detector_group, group_index ) in state.detector_histograms">
          <p class="center text-sm">{{ detector_group.gname }}</p>
          <div v-if="detector_group.gname && detector_group.histograms">
            <div v-for="( hist, hist_index ) in detector_group.histograms"
              class="rounded-md shadow bg-sky-50 hover:bg-slate-300">
              <p class="mb-0 text-xs">{{ hist.name }}</p>
              <div v-if="hist.name && hist.data">
                <!-- DOM ID: gname(detector group name) + histogram name + hist index; which gives unique id-->
                <div class="object-center w-full h-40 mb-6 rounded"
                  v-bind:id="detector_group.gname + hist.name + hist_index">
                  {{
                    drawHistJson(
                      detector_group.gname + hist.name + hist_index,
                      hist.data
                    )
                  }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
<style></style>
