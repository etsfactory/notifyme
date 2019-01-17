<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <h2 class="modal-title">
        <i class="fas fa-envelope"></i>
        {{ text }} template
      </h2>
      <vue-form-generator
        @validated="onValidated"
        class="template-form"
        tag="form"
        :schema="schema"
        :model="model"
        :options="formOptions"
      ></vue-form-generator>
    </div>
  </div>
</template>

<script>
import templatesApi from "@/logic/templates";

export default {
  name: "ConfirmModal",
  props: {
    visible: Boolean,
    edit: Boolean,
    model: {
      type: Object,
      default: () => ({
        id: "",
        name: "",
        subject: "",
        text: ""
      })
    }
  },
  data: () => ({
    formValid: false,
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
          label: "Name",
          model: "name",
          placeholder: "John Doe",
          required: true,
          featured: true,
        },
        {
          type: "input",
          inputType: "text",
          label: "Subject",
          model: "subject",
          placeholder: "Subject of the email",
          required: true,
          featured: true,
          validator: "string"
        },
        {
          type: "textArea",
          rows: 10,
          inputType: "text",
          label: "Body",
          model: "text",
          placeholder: "Body of the email",
          featured: true,
          required: true,
          validator: "string"
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
  methods: {
    close() {
      this.$emit("update:visible", false);
    },
    async createTemplate() {
      for (var propName in this.model) {
        if (
          this.model[propName] === null ||
          this.model[propName] === undefined ||
          this.model[propName] === ""
        ) {
          delete this.model[propName];
        }
      }
      await templatesApi.post(this.model);
      this.$emit("update:visible", false);
      this.$emit("created");
    },
    async editTemplate() {
      await templatesApi.put(this.model)
      this.$emit("update:visible", false);
      this.$emit("created");
    },
    onValidated(isValid, errors) {
      this.isValid = isValid;
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
      onSubmit: () => (this.edit ? this.editTemplate() : this.createTemplate())
    });
  }
};
</script>

<style lang="scss" scoped>
.template-form /deep/ .field-input {
  width: 60%;
  display: block;
  margin: 1rem auto;
}
.template-form /deep/ .field-textArea {
  width: 100% !important;
  display: block;
  margin: 1rem auto;
}
.template-form {
  width: 100%;
}
.modal-inner {
  width: 40%;
  max-width: 40%;
}
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
