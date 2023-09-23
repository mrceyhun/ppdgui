import axios from "axios";
import { defineStore } from "pinia";

export const usePlotsStore = defineStore("plots", {
  state: () => ({
    // /* Holds all histograms of detector groups */
    resp_groups_data: [],
    resp_runs: [],
    resp_groups: [],
    resp_eras: [],
    error: "",
    hasUpdated: true,
    availableEras: [],
    inputSelectedEras: [],
    inputSelectedRuns: [],
    inputSelectedGroups: [],
  }),
  actions: {
    async getHistorgrams(argEras, argGroups, argRuns) {
      /* Prepare request object */
      const request = { eras: argEras, groups: argGroups, runs: argRuns };
      console.log("Request obj:" + JSON.stringify(request));
      try {
        const r = await axios.post("/v1/get-hists", request);
        const data = await r.data;

        /* Nested obj reactivity is not working, so we use v-if="hasUpdated" */
        this.hasUpdated = false;

        /* r.data: backend/api_v1/models.py : ResponseMain */
        this.resp_groups_data = await data.groups_data;
        this.resp_runs = await data.runs;
        this.resp_groups = await data.groups;
        this.resp_eras = await data.eras;
        this.hasUpdated = true;

        // TODO: use only on debug
        // console.log("Response: " + JSON.stringify(this.groups_data));
      } catch (e) {
        alert("No histograms found with given request");
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
    async getEras() {
      try {
        const r = await axios.get("/v1/get-eras");
        this.availableEras = await r.data;
        console.log("Response: " + JSON.stringify(this.availableEras));
      } catch (e) {
        if (e.response) {
          console.log("Error", JSON.stringify(e.response));
          console.log(e.message);
        } else {
          console.log("Error", e.message);
        }
      }
    },
    updateHistograms() {
      this.getHistorgrams(
        this.inputSelectedEras,
        this.inputSelectedGroups,
        this.inputSelectedRuns
      );
    },
  },
});
