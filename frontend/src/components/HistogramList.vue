<script setup>
// import Histogram from './Histogram.vue';
import { useRootHistogramStore } from '../stores/RootHistogramStore';
import axios from "axios";
import { computed } from 'vue';
import { gStyle, draw, parse as jsrootParse } from 'jsroot';

const store = useRootHistogramStore();

const histograms = computed(() => {

  // TODO Filters

  return store.rootHists;
});

async function drawHistJson(histJsonPath, domId) {
  // let obj = await httpRequest(histJsonPath, 'object');
  // console.log('Read object of type', obj._typename);
  // draw(domId, obj, "hist");
  const response = await axios.get(histJsonPath);
  let obj = jsrootParse(response.data);
  console.log('Read object of type', obj._typename, domId);
  return draw(domId, obj, "hist");
}

</script>
<template>
  <section class="bg-gray-100 py-2">
    <div class="container mx-auto px-2">
      <!-- TODO solve this h w issue! -->
      <div class="grid grid-flow-col auto-cols-min">
        <div class="token-item" v-for="( item, index ) in histograms" >
          <div class="grid-flow-row object-none h-48 w-96" v-bind:id="item.id">{{ drawHistJson(item.histImg, item.id) }}</div>
        </div>
      </div>

    </div>

  </section>
</template>
