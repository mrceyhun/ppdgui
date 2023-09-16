import { defineStore } from "pinia";
import axios from "axios";

export const useMainRunStore = defineStore("mainRun", {
  state: () => ({
    /* Holds all histograms of detector groups */
    runNumber: 0,
    runYear: 0,
    detectorHistograms: [],
    error: "",
    inputRunNumber: 0,
    hasUpdated: true,
  }),
  actions: {
    async getRunHistorgrams(argRunNumber) {
      try {
        const r = await axios.post("/v1/get-run-hists", {
          run_number: argRunNumber,
        });
        const data = await r.data;

        /* Nested obj reactivity is not working, so we use v-if="hasUpdated" */
        this.hasUpdated = false;

        /* r.data: { run_number: 0, run_year: 0, detector_histograms: [] } */
        this.detectorHistograms = await data.detector_histograms;
        this.runNumber = data.run_number;
        this.runYear = data.run_year;

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
    },
    updateRunNumber(run) {
      this.getRunHistorgrams(run);
      this.inputRunNumber = run;
    },
  },
});
