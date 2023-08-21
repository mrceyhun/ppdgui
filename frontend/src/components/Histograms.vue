<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import { drawHistJson } from '../stores/utils'


const rootFile = ref('downloads/dqm.root')
const resp = ref({})
const dirs = ref([])
const histograms = ref([])


async function fetchRootData() {
  dirs.value = null
  const res = await axios.post("/v1/get-root-hist-or-dirs",
    {
      "file_path": rootFile.value,
      "obj_path": "DQMData/Run 366713/EcalPreshower/Run summary/ESRecoSummary",
      "all_hists": true
    });
  resp.value = await res.data
  dirs.value = await resp.value.dirs;
  histograms.value = await resp.value.hist_json;
}


fetchRootData();
watch(rootFile, fetchRootData);

</script>

<!-- <template>
  <div v-if="dirs">
    <ul v-if="dirs.length">
      <li v-for="dir of dirs">- {{ dir }}</li>
    </ul>
  </div>

  <div v-if="histograms">
    <div class="token-item" v-for="( hist, index ) in histograms">
      {{ histograms[0].name }}
      <div v-if="hist.name && hist.data">
        <div class="grid-flow-row object-none h-48 w-96" v-bind:id="hist.name">
          {{ drawHistJson(hist.data, hist.name) }}
        </div>
      </div>
    </div>

  </div>
</template> -->

<template>
  <div v-if="histograms" id="histograms">
    <main class="container px-8 pt-10 mx-auto lg:px-20 grid grid-cols-1 md:grid-cols-3 gap-4">
      <div v-for="( hist, index ) in histograms">
        <div v-if="hist.name && hist.data" class="px-4 py-6 rounded-md shadow bg-sky-50 hover:bg-slate-300">
          <p class="mb-1 text-md lg:text-lg">{{ histograms[0].name }}</p>
          <div class="object-center w-full h-40 mb-6 rounded" v-bind:id="hist.name">
            {{ drawHistJson(hist.data, hist.name) }}
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
<style></style>