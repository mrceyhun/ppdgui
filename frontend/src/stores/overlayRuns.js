import { defineStore } from "pinia";
import axios from "axios";

export const useOverlayRunsStore = defineStore("overlayRuns", {
  state: () => ({
    /* Holds all histograms of detector groups */
    runNumbers: [],
    detectorHistograms: [],
    error: "",
    inputRunNumbers: [],
    hasUpdated: true,
  }),
  actions: {
    async getOverlayHistorgrams(argListRunNumbers) {
      console.log(JSON.stringify(argListRunNumbers));
      if (argListRunNumbers.length >= 2) {
        try {
          const r = await axios.post("/v1/get-overlay-hists", {
            run_numbers: argListRunNumbers,
          });
          const data = await r.data;

          /* Nested obj reactivity is not working, so we use v-if="hasUpdated" */
          this.hasUpdated = false;

          /* r.data: { run_number: 0, run_year: 0, detector_histograms: [] } */
          this.detectorHistograms = await data.detector_histograms;
          this.runNumbers = data.run_numbers;
          this.hasUpdated = true;

          // TODO: use only on debug
          // console.log("Response: " + JSON.stringify(this.detectorHistograms));
        } catch (e) {
          alert("No histograms found with this Run Number");
          if (e.response) {
            console.log("Error", e.response.data.detail);
            this.error = e.response.data.detail;
            console.log(e.message);
          } else if (e.request) {
            console.log(e.request);
          } else {
            console.log("Error", e.message);
          }
        }
      }
    },
    updateOverlayRunNumbers(runs) {
      this.getOverlayHistorgrams(runs);
      this.inputRunNumbers = runs;
    },
  },
});
