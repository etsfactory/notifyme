<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <h2 class="modal-title">
        <i class="fas fa-filter"></i> Create new bus filter
      </h2>
      <vue-form-generator
        @validated="onValidated"
        class="user-form"
        tag="form"
        :schema="schema"
        :model="model"
        :options="formOptions"
      ></vue-form-generator>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateBusFilter",
  props: {
    visible: Boolean,
    title: {
      type: String,
      default: "Are you sure?"
    }
  },
  data: () => ({
    busFilterApi: "/bus_filters",
    formValid: false,
    model: {
      id: "",
      exchange: "",
      key: "",
      exchange_type: "fannout",
      durable: false,
      description: "",
      category: ""
    },
    schema: {
      fields: [
        {
          type: "input",
          inputType: "text",
          label: "ID",
          model: "id"
        },
        {
          type: "input",
          inputType: "exchange",
          label: "Exchange",
          model: "exchange",
          placeholder: "Bus exchange",
          requiered: true,
          min: 1,
          validator: "string",
          featured: true
        },
        {
          type: "input",
          inputType: "string",
          label: "Key",
          model: "key",
          placeholder: "Key for the exchange"
        },
        {
          type: "select",
          label: "Exchange type",
          model: "exchange_type",
          values: ["fannout", "direct"]
        },
        {
          type: "checkbox",
          label: "Durable",
          model: "durable",
          default: false
        },
        {
          type: "input",
          inputType: "string",
          label: "Description",
          model: "description",
          placeholder: "Description"
        },
        {
          type: "input",
          inputType: "string",
          label: "Category",
          model: "category",
          placeholder: "Category"
        }
      ]
    },
    formOptions: {
      validateAfterChanged: true,
      validateAsync: true
    }
  }),
  methods: {
    close() {
      this.$emit("update:visible", false);
    },
    createBusFilter() {
      for (var propName in this.model) {
        if (
          this.model[propName] === null ||
          this.model[propName] === undefined ||
          this.model[propName] === ""
        ) {
          delete this.model[propName];
        }
      }
      const busFiltersEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST + this.busFilterApi;
      axios.post(busFiltersEndpoint, this.model).then(() => {
        this.$emit("update:visible", false);
        this.$emit("created");
      });
    },
    onValidated(isValid, errors) {
      this.isValid = isValid;
    }
  },
  created() {
    this.schema.fields.push({
      type: "submit",
      buttonText: "Create",
      validateBeforeSubmit: true,
      styleClasses: "button-submit",
      onSubmit: () => this.createBusFilter()
    });
  }
};
</script>

<style lang="scss" scoped>
.modal .modal-title {
  font-size: 1.8rem;
}
.modal /deep/ .button-submit {
  margin-top: 2rem;
  margin-bottom: 0;
  text-align: center;
}
.modal /deep/ .button-submit input {
  margin: 0px auto !important;
}
</style>
