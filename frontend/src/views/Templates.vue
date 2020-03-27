<template>
  <div class="templates">
    <the-header>
      <template slot="title">Templates</template>
      <template slot="buttons">
        <button class="button-main" @click="createTemplate">
          <img svg-inline class="icon create-icon" src="../assets/icons/plus.svg">Create template
        </button>
      </template>
    </the-header>

    <error v-if="error" :error="error"/>
    <template-table v-if="templates" :templates="templates" @deleted="showModal"/>
    <confirm-modal :visible.sync="showDeleteModal" @accept="deleteTemplate"/>
    <create-template :visible.sync="showCreateModal" @created="getTemplates"/>
  </div>
</template>

<script>
import templatesApi from "@/logic/templates";

import TemplateTable from "@/components/TemplateTable.vue";
import ConfirmModal from "@/components/ConfirmModal.vue";
import TheHeader from "@/components/TheHeader.vue";
import CreateTemplate from "@/components/CreateTemplate.vue";
import Error from "@/components/Error.vue";

export default {
  name: "Templates",
  components: {
    TemplateTable,
    ConfirmModal,
    CreateTemplate,
    TheHeader,
    Error
  },
  data: () => ({
    templates: null,
    showDeleteModal: false,
    selectedTemplate: null,
    showCreateModal: false,
    error: null
  }),
  created() {
    this.getTemplates();
  },
  methods: {
    async getTemplates() {
      try {
        let response = await templatesApi.getAll();
        this.templates = response.data;
      } catch (error) {
        this.error = error.response;
      }
    },
    showModal(template_id) {
      this.showDeleteModal = true;
      this.selectedTemplate = template_id;
    },
    async deleteTemplate() {
      this.showDeleteModal = false;
      try {
        await templatesApi.delete(this.selectedTemplate);
      } catch (error) {
        this.error = error.response;
      }
      this.getTemplates();
    },
    createTemplate() {
      this.showCreateModal = true;
    }
  }
};
</script>

<style lang="scss" scoped>
.templates {
  position: relative;
}
</style>
