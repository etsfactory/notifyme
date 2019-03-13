<template>
  <div>
    <error v-if="error" :error="error"/>
    <div v-if="template">
      <the-header>
        <template slot="title">Template</template>
        <template slot="buttons">
          <router-link to="/bus_filters" class="link">
            <i class="fas fa-chevron-left"></i>Back to templates
          </router-link>
        </template>
      </the-header>
      <div class="template">
        <div class="template-container">
          <div class="buttons">
            <action-buttons @edit="showEditModal" @remove="showDeleteTemplate = true"></action-buttons>
            <confirm-modal
              :visible.sync="showDeleteTemplate"
              @accept="deleteTemplate"
              subtitle="This action can not be undone. All bus filters asociated with this template will be replaced with default template"
            />
            <key-value-table class="info" :data="template" disable="text"/>
          </div>
        </div>
        <div class="right">
          <div class="text">
            <h2>Body of the email:</h2>
            <pre v-highlightjs>
          <code class="html text-body">{{textHTML}}</code>
        </pre>
          </div>
          <create-template
            :model="template"
            :visible.sync="showCreateModal"
            :edit="true"
            @created="$router.go(0)"
            :code="textHTML"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import templatesApi from "@/logic/templates";
import beautify from "js-beautify";
import KeyValueTable from "@/components/KeyValueTable.vue";
import TheHeader from "@/components/TheHeader.vue";
import ActionButtons from "@/components/ActionButtons.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import CreateTemplate from "@/components/CreateTemplate.vue";
import Error from "@/components/Error.vue";

export default {
  name: "BusFilter",
  components: {
    KeyValueTable,
    ActionButtons,
    ConfirmModal,
    TheHeader,
    CreateTemplate,
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
    }
  }
};
</script>

<style lang="scss" scoped>
.header {
  width: 24%;
}
.template {
  position: relative;
  display: flex;
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
.users {
  margin-top: 3rem;
}
.template-container {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-right: 3rem;
}
.buttons {
  width: 100%;
}
.text-body {
  padding: 1rem 2rem;
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
.right {
  width: 75%;
  margin-top: -4.98rem;
}
.link {
  text-decoration: none;
  color: #828282;
}
.fa-chevron-left {
  color: $color-main;
  margin-right: 0.5rem;
}
</style>
