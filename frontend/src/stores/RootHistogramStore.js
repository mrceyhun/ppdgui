import axios from "axios";
import { reactive } from 'vue';

import { parse as jsrootParse } from 'jsroot';
export const store = reactive({
  confDir: '',
  hists: [],
})


// export const store = reactive({
//   confDir: 'xxx',
//   data() {
//     return {
//       confDir: 
//     }
//   },
//   methods: {
//     getDirs() {
//       axios
//         .post("/get-json-file", { params: { q: this.confDir.mainPath } })
//         .then((response) => console.log(response))
//     }
//   }
// })