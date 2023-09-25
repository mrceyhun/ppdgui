<script setup>
import { usePlotsStore } from "@/stores/plots.js";
import { storeToRefs } from "pinia";
import { ref } from 'vue';

const plotsStore = usePlotsStore();

/* Make store variable reflective */
const { limitMaxEraRunSizePerGroup } = storeToRefs(plotsStore)
const inputMaxRunPerEra = ref(limitMaxEraRunSizePerGroup); // Set default value

/* On input hit enter */
function submit() {
  const val = parseInt(inputMaxRunPerEra.value);
  if (val > 50) {
    alert("Max run size per ERA cannot exceed 50 for performance issues!")
    return;
  }
  plotsStore.updateMaxEraRunSize(parseInt(inputMaxRunPerEra.value));
}

</script>

<template>
  <div>

    <div class="grow text-ellipsis line-clamp-1">

      <span for="input-run-size" class="block text-xs font-medium text-white">Max era run size per group:</span>

      <input
        @keyup.enter="submit" id="input-run-size"
        v-model.lazy.number="inputMaxRunPerEra" maxLength="3" type="number"
        oninput="javascript: if (this.value.length > this.maxLength) this.value = this.value.slice(0, this.maxLength);"
        class="block w-full px-2 py-0 text-sm rounded-lg bg-gray-50 border border-gray-300 text-gray-900 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        required>

    </div>
  </div>
</template>
