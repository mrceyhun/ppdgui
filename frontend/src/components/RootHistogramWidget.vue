<script setup>
import { draw, parse as jsrootParse } from 'jsroot';

defineProps({
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
async function drawHistJson(domId, jsonData, histType) {
  const obj = await jsrootParse(jsonData);
  // console.log('Read object of type', histJson, domId);
  switch (histType) {
    case 'TH1F':
      return await draw(domId, obj, "hist");
    case 'TH2F':
      return await draw(domId, obj, "colz");
    case 'TCanvas':
      return await draw(domId, obj, "hist");
    default:
      console.log(`Cannot draw ROOT class type of ${histType}. Drawing default "hist".`);
      return await draw(domId, obj, "hist");
  }
}
</script>

<template>
  <!-- Height(h-48	height: 12rem; /* 192px */) Width( depends on how many columns in the row: grid-cols-N) -->
  <div v-bind:id="name" class="object-center h-48 w-full flex mb-1 rounded">
    {{ drawHistJson(name, data, type) }}
  </div>
</template>
