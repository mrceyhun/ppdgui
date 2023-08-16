import { defineStore } from "pinia";
import axios from "axios";
import { ref } from "vue";


export const useRootHistogramStore = defineStore("rootHists", {
  state: () => ({
    rootHists: ref([]),
    loading: false,
    // TODO change names
    selectedBrand: "All",
    selectedGender: "All",
    selectedPrice: "All",
    selectedType: "All",
  }),

  actions: {
    async getHistograms() {
      const URL = "/data.json";
      this.loading = true;
      const response = await axios.get(URL);
      this.rootHists = await response.data;
      this.loading = false;
    },
  },
});
