import { defineStore } from "pinia";
import axios from "axios";

export const useMainRunStore = defineStore("mainRun", {
  state: () => ({
    /* Holds all histograms of detector groups */
    runNumber: 0,
    runYear: 0,
    detectorHistograms: [],
    error: "",
  }),

  actions: {
    async getRunHistorgrams(argRunYear, argRunNumber) {
      try {
        const r = await axios.post("/v1/get-histogram-jsons", {
          run_year: argRunYear,
          run_number: argRunNumber,
        });
        const data = await r.data;
        /* r.data: { run_number: 0, run_year: 0, detector_histograms: [] } */
        console.log(data);
        this.detectorHistograms = await data.detector_histograms;
        this.runNumber = data.run_number;
        this.runYear = data.run_year;

        console.log("Response: " + JSON.stringify(this.detectorHistograms));
      } catch (e) {
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
  },
});