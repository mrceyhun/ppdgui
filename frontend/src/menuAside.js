import {
  mdiMonitor,
  mdiGithub,
  mdiViewList,
} from "@mdi/js";

export default [
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
        label: "Item One",
      },
      {
        label: "Item Two",
      },
    ],
  },
  {
    href: "https://github.com/mrceyhun/ppdgui",
    label: "GitHub",
    icon: mdiGithub,
    target: "_blank",
  },
];
