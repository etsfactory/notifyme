<template>
  <div class="template">
    <h1>
      <i class="fas fa-envelope"></i> Template
    </h1>
    <error v-if="error" :error="error"/>
    <div v-if="template">
      <div class="template-container">
        <key-value-table class="info" :data="template" disable="text"/>
        <div class="buttons">
          <action-buttons @edit="showEditModal" @remove="showDeleteTemplate = true"></action-buttons>
          <confirm-modal
            :visible.sync="showDeleteTemplate"
            @accept="deleteTemplate"
            subtitle="This action can not be undone"
          />
        </div>
      </div>
      <div class="text">
        <h2>Body of the email:</h2>
        <pre v-highlightjs>
          <code
  class="html text-body"
  @blur="onTextEdit"
  :class="{'editing-code': editingText}"
  @click="editText"
  contenteditable
>{{textHTML}}</code>
        </pre>
        <button v-if="editingText" class="button-main button-edit" @click="saveTemplate">Save</button>
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
import templatesApi from "@/logic/templates";
import beautify from "js-beautify";
import KeyValueTable from "@/components/KeyValueTable.vue";
import ActionButtons from "@/components/ActionButtons.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateTemplate from "@/components/CreateTemplate.vue";
import SubscriptionModal from "@/components/SubscriptionModal.vue";
import Error from "@/components/Error.vue";

export default {
  name: "BusFilter",
  components: {
    KeyValueTable,
    ActionButtons,
    ConfirmModal,
    CreateTemplate,
    SubscriptionModal,
    Error
  },
  data: () => ({
    template: null,
    showConfirmModal: false,
    showCreateModal: false,
    showSubscriptionModal: false,
    showDeleteTemplate: false,
    textHTML: "",
    editedText: "",
    editingText: false,
    error: null
  }),
  created() {
    this.getTemplate();
  },
  methods: {
    async getTemplate() {
      try {
        let response = await templatesApi.get(this.$route.params.id);
        this.template = response.data;
        let text_breaks = response.data.text
          .replace(/(\r\n\t|\n|\r\t)/gm, "")
          .replace(/{%/g, "\n{%")
          .replace(/%}/g, "%}\n");
        this.textHTML = beautify.html(text_breaks, {
          indent_size: 2,
          wrap_line_length: 100
        });
      } catch (error) {
        this.error = error.response;
      }
    },
    async saveTemplate() {
      try {
        this.template.text = String(this.editedText).replace(
          /(\r\n\t|\n|\r\t)/gm,
          ""
        );
        await templatesApi.put(this.template);
        this.getTemplate();
      } catch (error) {
        this.error = error.response;
      }
    },
    async deleteTemplate() {
      try {
        await templatesApi.delete(this.template.id);
        this.$router.push("/templates");
      } catch (error) {
        this.error = error.response;
      }
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
  padding: 0.5rem;
}
.button-grey {
  margin-left: 1rem;
}
.button-edit {
  margin-top: -3rem;
}
pre {
  margin: 0;
}
</style>
