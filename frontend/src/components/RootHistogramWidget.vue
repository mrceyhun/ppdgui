<script setup>
import { ref } from 'vue';
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


/* TODO: evaluate sync function */
async function drawHistJson(domId, histJson) {
  const obj = await jsrootParse(histJson);
  // console.log('Read object of type', histJson, domId);
  return draw(domId, obj, "hist");
}

</script>

<template>
  <div v-bind:id="name" class="object-center w-full h-40 mb-6 rounded">
    <!-- <span v-show="isReady"
      class="animate-spin inline-block w-4 h-4 border-[3px] border-current border-t-transparent text-blue-600 rounded-full"
      role="status" aria-label="loading">
      <span class="sr-only">Loading...</span>
    </span> -->

    {{ drawHistJson(name, data) }}

  </div>
</template>
