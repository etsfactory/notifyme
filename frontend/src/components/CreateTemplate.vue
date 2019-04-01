<template>
  <div v-show="visible" class="modal" id="modal" :class="{hide: !visible}">
    <div class="modal-bg" @click="close"></div>
    <div class="modal-inner">
      <a class="modal-close" @click="close">X</a>
      <h2 class="modal-title">
        <i class="fas fa-envelope"></i>
        {{ text }} template
      </h2>
      <error v-if="error" :error="error"/>
      <p class="center">* If an id is not provided automatically an id will be generated.</p>
      <p class="center">ID cannot be change.</p>
      <vue-form-generator
        @validated="onValidated"
        class="template-form"
        tag="form"
        :schema="schema"
        :model="model"
        :options="formOptions"
      ></vue-form-generator>
      <pre class="code" v-highlightjs>
          <code class="html text-body" @blur="onTextEdit" @click="editText" contenteditable>{{placeholder}}
          </code>
        </pre>
      <button
        class="button-main button-submit button-template"
        @click="edit ? editTemplate() : createTemplate()"
      >{{text}}</button>
    </div>
  </div>
</template>

<script>
import templatesApi from "@/logic/templates";
import Error from "@/components/Error.vue";

export default {
  name: "ConfirmModal",
  components: {
    Error
  },
  props: {
    visible: Boolean,
    edit: Boolean,
    code: String,
    httpCall: {
      type: Boolean,
      default: true
    },
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
    error: null,
    editingText: false,
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
          placeholder: "Logs",
          required: true,
          featured: true
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
    },
    placeholder() {
      return this.edit ? this.code : "HTML code of the email";
    }
  },
  created() {
    if (this.edit) {
      this.schema.fields[0].disabled = true;
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
      try {
        if (this.httpCall) {
          this.model.text = this.model.text.replace(/(\r\n\t|\n|\r\t)/gm, "");
          await templatesApi.post(this.model);
          this.$emit("update:visible", false);
          this.$emit("created");
        } else {
          this.$emit("created", this.model);
        }
      } catch (error) {
        this.error = error.response;
      }
    },
    async editTemplate() {
      try {
        this.model.text = this.model.text.replace(/(\r\n\t|\n|\r\t)/gm, "");
        await templatesApi.put(this.model);
        this.$emit("update:visible", false);
        this.$emit("created");
      } catch (error) {
        this.error = error.response;
      }
    },
    editText() {
      this.editingText = true;
    },
    onTextEdit(event) {
      this.model.text = event.target.innerText;
    },
    cancelEditText() {
      this.editingText = false;
    },
    onValidated(isValid) {
      this.isValid = isValid;
    }
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
.code {
  max-width: 100%;
  width: 100%;
  padding: 0 10px;
}
.code code {
  max-width: 100%;
  background-color: white;
  border: 1px solid grey;
  border-radius: 10px;
  min-height: 300px;
}
</style>
