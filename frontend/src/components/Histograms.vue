<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import { drawHistJson } from '../stores/utils'


const rootFile = ref('')
const errorMessage = ref('')
const rootObjPath = ref('')
const resp = ref('')


async function fetchRootData() {
  console.log(rootFile.value);
  console.log(rootObjPath.value);

  try {
    errorMessage.value = null;
    const response = await axios.post("/v1/get-root-hist-or-dirs",
      {
        "file_path": rootFile.value,
        "obj_path": rootObjPath.value,
        "all_hists": true
      });
    resp.value = await response.data;
    // dirs.value = await response.value.dirs;
    // histograms.value = await resp.value.hist_json;
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


// fetchRootData();
// watch(rootFile, fetchRootData);

</script>
<template>
  <!-- {{ resp }} -->
  <div class="px-8 pt-2 mx-auto lg:px-40 gap-4">
    <form @submit.prevent="fetchRootData" class="grid items-end gap-6 md:grid-cols-3">
      <div class="relative">
        <input v-model="rootFile" type="text" id="input_root_file_path"
          class="border border-10 border-gray-800 px-2.5 pb-2 pt-4 w-full text text-gray-900 rounded-lg focus:outline-none focus:ring-0 focus:border-blue-600 peer"
          placeholder=" " />
        <label for="input_root_file_path"
          class="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1">
          ROOT File EOS Path
        </label>
        <p id="floating_helper_text" class="mt-2 text-xs text-gray-500">Please provide EOS directory for test</p>
      </div>
      <div class="relative">
        <input v-model="rootObjPath" type="text" id="input_root_obj_path"
          class="border border-10 border-gray-800 px-2.5 pb-2 pt-4 w-full text text-gray-900 rounded-lg focus:outline-none focus:ring-0 focus:border-blue-600 peer"
          placeholder=" " />
        <label for="input_root_obj_path"
          class="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1">
          TDirectory Path Inside ROOT File
        </label>
        <p id="floating_helper_text" class="mt-2 text-xs text-gray-500">Please provide the TDirectory inside the ROOT file
        </p>
      </div>
      <div class="relative md:flex md:items-center mb-6">
        <button
          class="shadow bg-purple-500 hover:bg-purple-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded">
          Show
        </button>
      </div>

    </form>
    <!-- ERROR MESSAGE -->
    <div v-if="errorMessage" id="dirs">
      <div class="p-4 mb-4 text-sm text-yellow-800 rounded-lg bg-yellow-50  " role="alert">
        <span class="font-medium">Warning alert!</span> {{ errorMessage }}
      </div>
    </div>
    <!-- THERE ARE NO HISTOGRAMS, ONLY DIRECTORIES -->
    <div v-else-if="resp.dirs" id="dirs">
      There are only directories: {{ resp.dirs }}
    </div>
    <!-- SHOW HISTOGRAMS -->
    <div v-else-if="resp.hist_json" id="histograms">
      <main class="container px-8 pt-10 mx-auto lg:px-20 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="( hist, index ) in resp.hist_json">
          <!-- CHECK AGAIN THE RESPONSE SCHEMA, SEE: backend/api_v1/models.py ResponseRootObj-->
          <div v-if="hist.name && hist.data" class="px-4 py-6 rounded-md shadow bg-sky-50 hover:bg-slate-300">
            <p class="mb-1 text-md lg:text-lg">{{ resp.hist_json[0].name }}</p>
            <div class="object-center w-full h-40 mb-6 rounded" v-bind:id="hist.name">
              {{ drawHistJson(hist.data, hist.name) }}
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
<style></style>
