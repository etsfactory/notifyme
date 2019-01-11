<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <h2 class="modal-title">
        <i class="fas fa-user"></i> Create a new user
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
  name: "ConfirmModal",
  props: {
    visible: Boolean,
    title: {
      type: String,
      default: "Are you sure?"
    }
  },
  data: () => ({
    usersApi: "/users",
    formValid: false,
    model: {
      id: "",
      name: "",
      email: ""
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
          inputType: "text",
          label: "Name",
          model: "name",
          placeholder: "John Doe",
          featured: true,
        },
        {
          type: "input",
          inputType: "email",
          label: "E-mail",
          model: "email",
          placeholder: "johndoe@gmail.com",
          required: true,
          validator: "email"
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
    createUser() {
      const usersEndpoint = process.env.VUE_APP_NOTIFYME_HOST + this.usersApi;
      axios.post(usersEndpoint, this.model).then(() => {
        this.$emit("update:visible", false);
      })
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
      onSubmit: () => this.createUser()
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
