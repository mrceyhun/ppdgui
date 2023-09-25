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
    messageText: "",
    hasUpdated: true,
    limitMaxRunsPerEra: 5,
    availableGroups: [],
    availableEras: [],
    availableRunEraTuples: [],
    inputSelectedGroups: [],
    inputSelectedEras: [],
    inputSelectedRunEraTuples: [],
  }),
  actions: {
    async getHistorgrams(argGroups, argEras, argRuns) {
      /* Prepare request object */
      let msg = "";
      if (argGroups.length == 0) {
        msg += "Please select GROUP. ";
      } else if (argEras.length == 0) {
        msg += "Please select ERA. ";
      } else if (argEras.length == 0) {
        msg += "No RUN is selected. ";
      }

      if (msg !== "") {
        this.messageText = msg;
        return;
      }
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
        if (e.response) {
          console.log("Error", e.response.data.detail);
          this.error = e.response.data.detail;
          console.log(e.message);
        } else if (e.request) {
          console.log(e.request);
        } else {
          console.log("Error", e.message);
        }
        // INFORM
        this.messageText = e.message;
        return;
      }
      this.messageText = "";
    },
    async getAvailableGroups() {
      try {
        const r = await axios.get("/v1/get-groups");
        this.availableGroups = await r.data;

        /* DEFAULT: Make all GROUPS selected by default */
        this.inputSelectedGroups = await r.data;
        console.log(
          "Response available groups: " + JSON.stringify(this.availableGroups)
        );
      } catch (e) {
        if (e.response) {
          console.log("Error", JSON.stringify(e.response));
          console.log(e.message);
        } else {
          console.log("Error", e.message);
        }
        // INFORM
        this.messageText = e.message;
        return;
      }
      this.messageText = "";
    },
    async getAvailableEras() {
      /* Filtered by selected GROUPS */
      try {
        const r = await axios.get("/v1/get-eras", {
          params: {
            groups: this.inputSelectedGroups,
          },
          paramsSerializer: {
            indexes: null, // to make query parameters list like ?groups=AA&groups=BB&groups=CCC
          },
        });

        this.availableEras = await r.data;
        console.log(
          "Response available eras: " + JSON.stringify(this.availableEras)
        );
      } catch (e) {
        if (e.response) {
          console.log("Error", JSON.stringify(e.response));
          console.log(e.message);
        } else {
          console.log("Error", e.message);
        }
        this.messageText = e.message;
        return;
      }
      this.messageText = "";
    },
    async getAvailableRunEraTuples() {
      /* Filtered by selected GROUPS and ERAS */
      if (this.inputSelectedEras.length <= 0) {
        this.availableRunEraTuples = [];
        this.messageText = "Please select ERA.";
        return;
      }

      try {
        const r = await axios.get("/v1/get-runs", {
          params: {
            limit: this.limitMaxRunsPerEra,
            groups: this.inputSelectedGroups,
            eras: this.inputSelectedEras,
          },
          paramsSerializer: {
            indexes: null, // to make query parameters list like ?eras=AA&eras=BB
          },
        });

        this.availableRunEraTuples = await r.data;

        /* DEFAULT: Make all RUN:ERA tuples selected by default */
        this.inputSelectedRunEraTuples = await r.data;
        console.log(
          "Response available eras: " +
            JSON.stringify(this.availableRunEraTuples)
        );
      } catch (e) {
        if (e.response) {
          console.log("Error", JSON.stringify(e.response));
          console.log(e.message);
        } else {
          console.log("Error", e.message);
        }
        // INFORM
        this.messageText = e.message;
        return;
      }
      this.messageText = "";
    },
    updateHistograms() {
      this.getHistorgrams(
        this.inputSelectedGroups,
        this.inputSelectedEras,
        this.inputSelectedRunEraTuples.map((item) => {
          // Only Run numbers, drop Era names fro run:era tuples
          return item[0];
        })
      );
    },
  },
});
