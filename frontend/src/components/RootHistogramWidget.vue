<script setup>
import { draw, parse as jsrootParse } from 'jsroot';

defineProps({
  id: {
    type: String,
  },
  name: {
    type: String,
    default: null,
  },
  type: {
    type: String,
    default: null,
  },
  data: {
    type: String,
    default: null,
  },
});

/* JSROOT MAIN DRAW FUNCTION */
/* TODO: ZOOM CONTROL or savePng control https://root.cern/js/latest/api.htm#custom_html_zooming_src */

async function drawHistJson(domId, jsonData, histType) {
  const obj = await jsrootParse(jsonData);
  // console.log('[DEBUG] Read object of type', jsonData, domId);
  switch (histType) {
    case 'TH1F':
      return await draw(domId, obj, "hist");
    case 'TH2F':
      return await draw(domId, obj, "colz");
    case 'TCanvas':
      return await draw(domId, obj, "hist");
    case 'TProfile':
      return await draw(domId, obj, "hist");
    case 'THStack':
      return await draw(domId, obj, "hist");
    default:
      console.log(`[INFO] Cannot draw ROOT class type of ${histType}. Drawing default "hist".`);
      return await draw(domId, obj, "hist");
  }
}
</script>

<template>
  <!-- Height(h-48	height: 12rem; /* 192px */) Width( depends on how many columns in the row: grid-cols-N) -->
  <div v-bind:id="id" class="object-center h-48 w-full flex mb-1 rounded">
    {{ drawHistJson(id, data, type) }}
  </div>
</template>
