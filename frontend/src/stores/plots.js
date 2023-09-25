import axios from "axios";
import { defineStore } from "pinia";

export const usePlotsStore = defineStore("plots", {
  state: () => ({
    /* Holds all histograms of detector groups */
    resp_groups_data: [],
    /* Holds main error message for debugging */
    error: "",
    /* Holds the human readable error message for users. Bunded to Aside menu top "Msg:" text. */
    messageText: "",
    /* Controls if reactive data is updated and draws histograms accordingly. Nested objects cannot be reactive as we want. */
    hasUpdated: true,
    /* Controls of loading animation, different than hasUpdated */
    hasTriggeredToUpdate: true,
    /* Controls how many RUNs should be included per ERA. Returned RUNs are always the most recent RUNs. */
    limitMaxEraRunSizePerGroup: 5,
    /* Holds available detector Groups coming from backend */
    availableGroups: [],
    /* Holds available ERAs coming from backend */
    availableEras: [],
    /* Holds available RUN:ERA couples coming from backend */
    availableRunEraDict: [],
    /* Holds selected Groups from drop-down menu, default is ALL available Groups coming from backend. Each action(+/-) updates list of ERAs. */
    inputSelectedGroups: [],
    /* Holds selected ERAs from drop-down menu, default is none of them are selected, but can be changed. Each action(+/-) updates list of RUNs. */
    inputSelectedEras: [],
    /* Holds selected RUNs from drop-down menu, default is ALL for the selected ERAs. If no ERA is selected, user cannot see any value. Each action(+/-) updates all histograms. 
    Default value is keys of availableRunEraDict.
    */
    inputSelectedRuns: [],
  }),
  actions: {
    async getHistorgrams(argGroups, argEras, argRuns, argEraRunSizeLimit) {
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
      /* Request */
      const request = {
        eras: argEras,
        groups: argGroups,
        runs: argRuns,
        max_era_run_size: argEraRunSizeLimit,
      };

      // console.log("[DEBUG] Request obj:" + JSON.stringify(request));
      try {
        this.hasTriggeredToUpdate = false;
        const r = await axios.post("/v1/get-hists", request);
        const data = await r.data;
        this.hasUpdated = false;

        /* Nested obj reactivity is not working, so we use v-if="hasUpdated" */

        /* r.data: backend/api_v1/models.py : ResponseMain */
        this.resp_groups_data = await data.groups_data;
        this.hasTriggeredToUpdate = true;
        this.hasUpdated = true;
        // TODO: use only on debug
        // console.log("[DEBUG] Response: " + JSON.stringify(this.groups_data));
      } catch (e) {
        if (e.response) {
          // console.log("[INFO] Error", e.response.data.detail);
          this.error = e.response.data.detail;
          console.log("[INFO] ", e.message);
        } else if (e.request) {
          console.log("INFO", e.request);
        } else {
          console.log("[INFO] Error", e.message);
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
        // console.log("[DEBUG] Response available groups: " + JSON.stringify(this.availableGroups));
      } catch (e) {
        if (e.response) {
          // console.log("[DEBUG] Error", JSON.stringify(e.response));
          console.log("[INFO] ", e.message);
        } else {
          console.log("[INFO] Error", e.message);
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
        // console.log("[DEBUG] Response available eras: " + JSON.stringify(this.availableEras));
      } catch (e) {
        if (e.response) {
          // console.log("[DEBUG] Error", JSON.stringify(e.response));
          console.log("[INFO] ", e.message);
        } else {
          console.log("[INFO] Error", e.message);
        }
        this.messageText = e.message;
        return;
      }
      this.messageText = "";
    },
    async getAvailableRunEraDict() {
      /* Filtered by selected GROUPS and ERAS */
      if (this.inputSelectedEras.length <= 0) {
        this.availableRunEraDict = [];
        this.messageText = "Please select ERA.";
        return;
      }

      try {
        const r = await axios.get("/v1/get-runs", {
          params: {
            limit: this.limitMaxEraRunSizePerGroup,
            groups: this.inputSelectedGroups,
            eras: this.inputSelectedEras,
          },
          paramsSerializer: {
            indexes: null, // to make query parameters list like ?eras=AA&eras=BB
          },
        });

        this.availableRunEraDict = await r.data;

        /* DEFAULT: Make all RUNs selected by default */
        this.inputSelectedRuns = Object.keys(this.availableRunEraDict);

        /* UPDATE HISTOGRAMS*/
        if (this.inputSelectedRuns.length > 0) {
          this.updateHistograms();
        }

        // console.log("[DEBUG] Available run-era dict: " + JSON.stringify(this.availableRunEraDict));
        // console.log("[DEBUG] Selected runs: " + JSON.stringify(this.inputSelectedRuns));
      } catch (e) {
        if (e.response) {
          // console.log("[DEBUG] Error", JSON.stringify(e.response));
          console.log("[INFO] ", e.message);
        } else {
          console.log("[INFO] Error", e.message);
        }
        // INFORM
        this.messageText = e.message;
        return;
      }
      this.messageText = "";
    },
    async updateMaxEraRunSize(val) {
      this.limitMaxEraRunSizePerGroup = val;
      await this.getAvailableRunEraDict(); // Update runs with new limit
    },
    async updateHistograms() {
      await this.getHistorgrams(
        this.inputSelectedGroups,
        this.inputSelectedEras,
        this.inputSelectedRuns,
        this.limitMaxEraRunSizePerGroup
      );
    },
  },
});
