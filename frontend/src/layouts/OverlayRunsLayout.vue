<script setup>
import { ref } from "vue";
import { storeToRefs } from "pinia";
import { useRouter } from "vue-router";
import { containerMaxW } from "@/config.js";
import RootHistogramGroupRow from "@/components/RootHistogramGroupRow.vue";
import { useOverlayRunsStore } from "@/stores/overlayRuns.js";

const router = useRouter();
const isAsideMobileExpanded = ref(false);
const isAsideLgActive = ref(false);

router.beforeEach(() => {
  isAsideMobileExpanded.value = false;
  isAsideLgActive.value = false;
});

const overlayRunsStore = useOverlayRunsStore();

/* Nested obj reactivity is not working, so we use v-if="hasUpdated" */
const { hasUpdated, detectorHistograms } = storeToRefs(overlayRunsStore)
</script>

<template>
  <section class="p-0 px-0" :class="containerMaxW">

    <RootHistogramGroupRow
      v-if="hasUpdated"
      v-for="(detectorGroup, index) in detectorHistograms"
      :key="index"
      :histograms="detectorGroup.histograms"
      :group-name="detectorGroup.gname"
      :dataset="detectorGroup.dataset"
      root-file="" />

  </section>
</template>
