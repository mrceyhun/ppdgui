import { defineStore } from "pinia";
import axios from "axios";

export const useMainRunStore = defineStore("mainRun", {
  state: () => ({
    /* Holds all histograms of detector groups */
    runNumber: 0,
    runYear: 0,
    detectorHistograms: [],
    error: "",
    inputRunYear: 2023,
    inputRunNumber: 370775,
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
        this.detectorHistograms = await data.detector_histograms;
        this.runNumber = data.run_number;
        this.runYear = data.run_year;

        // TODO: on debug use console.log("Response: " + JSON.stringify(this.detectorHistograms));
        return true;
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
      return false;
    },
    async updateRunNumber(year, run) {
      const success = await this.getRunHistorgrams(year, run);

      // If successfull, update run number and return true
      if (success) {
        this.inputRunYear = year;
        this.inputRunNumber = run;
      }
      return success;
    },
  },
});
