import AppInput from "@/components/AppInput.vue";
import AppSelect from "@/components/AppSelect.vue";
import AppCheckbox from "@/components/AppCheckbox.vue";
import AppButton from "@/components/AppButton.vue";
import AppFormCard from "@/components/AppFormCard/AppFormCard.vue";
import AppTile from "@/components/AppTile.vue";

export default {
  install: (app, options) => {
    app.component("app-input", AppInput);
    app.component("app-select", AppSelect);
    app.component("app-checkbox", AppCheckbox);
    app.component("app-button", AppButton);
    app.component("app-form-card", AppFormCard);
    app.component("app-tile", AppTile);
  },
};
