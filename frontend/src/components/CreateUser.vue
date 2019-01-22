<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <h2 class="modal-title">
        <i class="fas fa-user"></i>
        {{ text }} user
      </h2>
      <error v-if="error" :error="error"/>
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
import usersApi from "@/logic/users";
import Error from "@/components/Error.vue";

export default {
  name: "ConfirmModal",
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
        name: "",
        email: ""
      })
    }
  },
  data: () => ({
    usersApi: "/users",
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
          label: "Name",
          model: "name",
          placeholder: "John Doe",
          featured: true
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
      onSubmit: () => (this.edit ? this.editUser() : this.createUser())
    });
  },
  methods: {
    close() {
      this.$emit("update:visible", false);
    },
    async createUser() {
      for (var propName in this.model) {
        if (
          this.model[propName] === null ||
          this.model[propName] === undefined ||
          this.model[propName] === ""
        ) {
          delete this.model[propName];
        }
      }

      try {
        await usersApi.post(this.model);
        this.$emit("update:visible", false);
        this.$emit("created");
      } catch (error) {
        this.error = error.response;
      }
    },
    async editUser() {
      try {
        await usersApi.put(this.model);
        this.$emit("update:visible", false);
        this.$emit("created");
      } catch (error) {
        this.error = error.response;
      }
    },
    onValidated(isValid, errors) {
      this.isValid = isValid;
      this.error = errors;
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
