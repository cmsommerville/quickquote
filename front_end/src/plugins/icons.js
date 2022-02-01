import {
  PlusCircleIcon,
  PlusIcon,
  MinusIcon,
  ArrowCircleDownIcon,
  ArrowCircleUpIcon,
  MenuIcon,
  PuzzleIcon,
  CogIcon,
  SearchIcon,
  SunIcon,
  StarIcon,
  SparklesIcon,
  MoonIcon,
  ShieldExclamationIcon,
} from "@heroicons/vue/outline";

export default {
  install: (app, options) => {
    app.component("plus-circle-icon", PlusCircleIcon);
    app.component("minus-icon", MinusIcon);
    app.component("arrow-circle-down-icon", ArrowCircleDownIcon);
    app.component("arrow-circle-up-icon", ArrowCircleUpIcon);
    app.component("menu-icon", MenuIcon);
    app.component("plus-icon", PlusIcon);
    app.component("puzzle-icon", PuzzleIcon);
    app.component("cog-icon", CogIcon);
    app.component("search-icon", SearchIcon);
    app.component("sun-icon", SunIcon);
    app.component("star-icon", StarIcon);
    app.component("sparkles-icon", SparklesIcon);
    app.component("moon-icon", MoonIcon);
    app.component("shield-exclamation-icon", ShieldExclamationIcon);
  },
};
