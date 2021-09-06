import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.teal.darken1, // #E53935
        secondary: colors.teal.lighten4, // #FFCDD2
        accent: colors.indigo.base, // #3F51B5
        softer: colors.teal.lighten4,
      },
    },
  },
});
