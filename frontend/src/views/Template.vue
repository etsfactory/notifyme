<template>
  <div class="template">
    <div v-if="template">
      <h1>
        <i class="fas fa-envelope"></i> Template
      </h1>
      <div class="template-container">
        <key-value-table class="info" :data="template" disable="text"/>
        <div class="buttons">
          <action-buttons @edit="showEditModal"></action-buttons>
        </div>
      </div>
      <div class="text">
        <h2>Body for the email:</h2>
        <button v-if="editingText" class="button-main" @click="saveTemplate">Save</button>
        <pre v-highlightjs>
          <code
  class="html text-body"
  @blur="onTextEdit"
  :class="{'editing-code': editingText}"
  @click="editText"
  contenteditable
>{{textHTML}}</code>
        </pre>
        {{editedText}}
      </div>
      <create-template
        :model="template"
        :visible.sync="showCreateModal"
        :edit="true"
        @created="getTemplate"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import beautify from "js-beautify";
import UsersTable from "@/components/UsersTable.vue";
import KeyValueTable from "@/components/KeyValueTable.vue";
import ActionButtons from "@/components/ActionButtons.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateTemplate from "@/components/CreateTemplate.vue";
import SubscriptionModal from "@/components/SubscriptionModal.vue";

export default {
  name: "BusFilter",
  components: {
    UsersTable,
    KeyValueTable,
    ActionButtons,
    ConfirmModal,
    CreateTemplate,
    SubscriptionModal
  },
  data: () => ({
    template: null,
    templatesApi: "/templates/",
    showConfirmModal: false,
    showCreateModal: false,
    showSubscriptionModal: false,
    textHTML: "",
    editedText: "",
    editingText: false
  }),
  created() {
    this.getTemplate(this.$route.params.id);
  },
  methods: {
    getTemplate() {
      const templateEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.templatesApi +
        this.$route.params.id;
      axios.get(templateEndpoint).then(response => {
        this.template = response.data;
        let text_breaks = this.template.text
          .replace(/{%/g, "\n{%")
          .replace(/%}/g, "%}\n");
        this.textHTML = beautify.html(text_breaks, {
          indent_size: 2,
          wrap_line_length: 100
        });
      });
    },
    showEditModal() {
      this.showCreateModal = true;
    },
    showDeleteModal(id) {
      this.showConfirmModal = true;
      this.selectedUser = id;
    },
    closeDeleteModal() {
      this.showConfirmModal = false;
    },
    editText() {
      this.editingText = true;
    },
    onTextEdit(event) {
      this.editedText = event.target.innerText;
    },
    cancelEditText() {
      this.editingText = false;
    },
    saveTemplate() {
      const templateEndpoint =
        process.env.VUE_APP_NOTIFYME_HOST +
        this.templatesApi +
        this.$route.params.id;
      let template = this.template;
      template.text = String(this.editedText);
      axios.put(templateEndpoint, template).then(() => {
        this.getTemplate();
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.template {
  position: relative;
}
.notifications-table /deep/.actions {
  text-align: center !important;
}
.icon {
  padding: 0 3rem;
  cursor: pointer;
  &:hover {
    color: $color-main-dark;
  }
}
.info {
  width: 40%;
}
.users {
  margin-top: 3rem;
}
.template-container {
  display: flex;
  align-items: center;
}
.buttons {
  width: 35%;
}
.text {
  margin-top: 2rem;
}
.text-body {
  transition: all 0.15s ease-in-out;
}
.editing-code {
  background-color: white;
  border: 2px solid $color-main;
}
.button-grey {
  margin-left: 1rem;
}
</style>
