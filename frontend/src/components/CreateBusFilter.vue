<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <h2 class="modal-title">
        <i class="fas fa-filter"></i>
        {{ text }} bus filter
      </h2>
      <error v-if="error" :error="error" />
      <p class="center">* If an id is not provided automatically an id will be generated.</p>
      <p class="center">ID cannot be change.</p>
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
import busFiltersApi from "@/logic/bus_filters";
import Error from "@/components/Error.vue";

export default {
  name: "CreateBusFilter",
  components: {
    Error
  },
  props: {
    visible: Boolean,
    edit: Boolean,
    model: {
      type: Object,
      default: () => ({
        id: "",
        exchange: "",
        key: "",
        exchange_type: "fanout",
        durable: true,
        description: "",
        category: ""
      })
    }
  },
  data: () => ({
    busFilterApi: "/bus_filters",
    formValid: false,
    error: null,
    schema: {
      fields: [
        {
          type: "input",
          inputType: "text",
          label: "ID",
          model: "id",
          placeholder: "1"
        },
        {
          type: "input",
          inputType: "text",
          label: "Exchange",
          model: "exchange",
          placeholder: "Bus exchange",
          required: true,
          validator: "string",
          featured: true
        },
        {
          type: "select",
          label: "Exchange type",
          model: "exchange_type",
          values: ["fanout", "direct"]
        },
        {
          type: "input",
          inputType: "text",
          label: "Key",
          model: "key",
          placeholder: "Key for the exchange"
        },
        {
          type: "checkbox",
          label: "Durable",
          model: "durable",
          default: true
        },
        {
          type: "input",
          inputType: "text",
          label: "Description",
          model: "description",
          placeholder: "Description"
        },
        {
          type: "input",
          inputType: "text",
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
  computed: {
    text() {
      return this.edit ? "Edit" : "Create";
    }
  },
  created() {
    if (this.edit) {
      this.schema.fields[0].disabled = true;
    }
    this.schema.fields.push({
      type: "submit",
      buttonText: this.text,
      validateBeforeSubmit: true,
      styleClasses: "button-submit",
      onSubmit: () =>
        this.edit ? this.editBusFilter() : this.createBusFilter()
    });
  },
  methods: {
    close() {
      this.$emit("update:visible", false);
    },
    async createBusFilter() {
      for (var propName in this.model) {
        if (
          (this.model[propName] === null ||
            this.model[propName] === undefined ||
            this.model[propName] === "") &&
          propName !== "key"
        ) {
          delete this.model[propName];
        }
      }
      try {
        await busFiltersApi.post(this.model);
        this.$emit("update:visible", false);
        this.$emit("created");
      } catch (error) {
        this.error = error.response;
      }
    },
    async editBusFilter() {
      try {
        await busFiltersApi.put(this.model);
        this.$emit("update:visible", false);
        this.$emit("created");
      } catch (error) {
        this.error = error.response;
      }
    },
    onValidated(isValid) {
      this.isValid = isValid;
    }
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
