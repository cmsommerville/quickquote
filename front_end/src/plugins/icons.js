import {
  PlusCircleIcon,
  PlusIcon,
  MinusIcon,
  PencilIcon,
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
  QuestionMarkCircleIcon,
  BadgeCheckIcon,
  CheckCircleIcon,
  ShieldCheckIcon,
  ShieldExclamationIcon,
  GlobeIcon,
  GlobeAltIcon,
  XIcon,
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
    app.component("question-mark-circle-icon", QuestionMarkCircleIcon);
    app.component("badge-check-icon", BadgeCheckIcon);
    app.component("check-circle-icon", CheckCircleIcon);
    app.component("shield-check-icon", ShieldCheckIcon);
    app.component("shield-exclamation-icon", ShieldExclamationIcon);
    app.component("globe-icon", GlobeIcon);
    app.component("globe-alt-icon", GlobeAltIcon);
    app.component("x-icon", XIcon);
    app.component("pencil-icon", PencilIcon);
  },
};
