<script setup>
import RootHistogramGroupRow from "@/components/RootHistogramGroupRow.vue";
import { containerMaxW } from "@/config.js";
import { usePlotsStore } from "@/stores/plots.js";
import { storeToRefs } from "pinia";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const isAsideMobileExpanded = ref(false);
const isAsideLgActive = ref(false);

router.beforeEach(() => {
  isAsideMobileExpanded.value = false;
  isAsideLgActive.value = false;
});

const plotsStore = usePlotsStore();

/* Nested obj reactivity is not working, so we use v-if="hasUpdated" */
const { hasUpdated, hasTriggeredToUpdate, resp_groups_data } = storeToRefs(plotsStore)
</script>

<template>
  <section class="p-0 px-0 " :class="[containerMaxW, (!hasTriggeredToUpdate) ? 'opacity-25' : '']">

    <RootHistogramGroupRow
      v-if="hasTriggeredToUpdate"
      v-for="(detectorGroup, index) in resp_groups_data"
      :key="index"
      :plots="detectorGroup.plots"
      :group-name="detectorGroup.group_name"
      :dataset="detectorGroup.dataset"
      root-file="" />

  </section>
</template>
