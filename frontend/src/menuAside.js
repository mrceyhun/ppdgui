import { mdiMonitor, mdiGithub, mdiViewList, mdiCounter } from "@mdi/js";

export default {
  run: {
    to: "/",
    icon: mdiCounter,
    label: "-RunNumber-", // will be replaced in HomeView
  },
  menu: [
    {}, // Run will be first index: 0
    {
      to: "/",
      icon: mdiMonitor,
      label: "Dashboard",
    },
    {
      label: "Dropdown",
      icon: mdiViewList,
      menu: [
        {
          labelFor: "runNumber",
          labelText: "runNumber",
          inputType: "number",
          inputId: "runNumber",
          inputPlaceholder: "3",
          maxlength: "9",
          isAsideInput: true,
        },
      ],
    },
    {
      href: "https://github.com/mrceyhun/ppdgui",
      label: "GitHub",
      icon: mdiGithub,
      target: "_blank",
    },
  ],
};
