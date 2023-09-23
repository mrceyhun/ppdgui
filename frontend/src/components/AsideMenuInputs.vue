<script setup>
import AsideMenuOptionEra from "@/components/AsideMenuOptionEra.vue";
import { usePlotsStore } from "@/stores/plots.js";
import { storeToRefs } from "pinia";

/* TODO: validation https://vuejs.org/guide/components/props.html#prop-validation*/
const props = defineProps({
  icon: {
    type: String,
    required: true,
  },
  item: {
    type: Object,
    required: true,
  },
});
const emit = defineEmits(["menu-click"]);

const plotsStore = usePlotsStore();
const { availableEras } = storeToRefs(plotsStore)

</script>

<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}
</style>
<template>
  <div class="px-2">

    <AsideMenuOptionEra :items="availableEras" />

  </div>
</template>
