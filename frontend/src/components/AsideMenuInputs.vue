<script setup>
import AsideMenuInputMaxRunSize from "@/components/AsideMenuInputMaxRunSize.vue";
import AsideMenuOptionEra from "@/components/AsideMenuOptionEra.vue";
import AsideMenuOptionGroup from "@/components/AsideMenuOptionGroup.vue";
import AsideMenuOptionRun from "@/components/AsideMenuOptionRun.vue";
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
const { messageText, availableGroups, availableEras, availableRunEraDict } = storeToRefs(plotsStore)

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
    <div class="border border-rose-500 h-12 text-xs text-white subpixel-antialiased hover:text-sm hover:h-12">
      Msg: {{ messageText }}
    </div>
    <div class="py-1"></div>
    <AsideMenuInputMaxRunSize />
    <div class="py-1"></div>
    <AsideMenuOptionGroup :items="availableGroups" />
    <div class="py-1"></div>
    <AsideMenuOptionEra :items="availableEras" />
    <div class="py-1"></div>
    <AsideMenuOptionRun :items="availableRunEraDict" />

  </div>
</template>
